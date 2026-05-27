#!/usr/bin/env python3

import argparse
from pathlib import Path

import torch
from diffusers import StableDiffusionXLPipeline


MODEL_ID = "SG161222/RealVisXL_V5.0"
NEGATIVE_PROMPT = (
    "cartoon, anime, illustration, painting, stylized, fantasy armor, medieval, "
    "sci-fi spaceship, cyberpunk neon, comic book, lowres, blurry, duplicate, "
    "extra limbs, extra fingers, malformed hands, deformed face, text, watermark, "
    "logo, frame, signature"
)

PROFILES = [
    {
        "name": "Panicked Attendee",
        "slug": "panicked-attendee",
        "seed": 11021,
        "prompt": (
            "cinematic realistic photo, inside a modern biomedical conference building after a catastrophic rupture, "
            "one frightened attendee in expensive business-casual clothes sheltering behind a reception counter, "
            "dust in the air, dim red emergency lights, polished concrete floor, branded signage, overturned lanyards and tote bags, "
            "face tense and exhausted but fully human, grounded horror, believable anatomy, in-world corporate setting"
        ),
    },
    {
        "name": "Office Hollow",
        "slug": "office-hollow",
        "seed": 11022,
        "prompt": (
            "cinematic realistic horror photo, recently ruptured Kallisto office worker in a torn blazer drifting through a high-end lobby, "
            "unfocused eyes, hanging jaw, hands reaching toward motion before the head turns, dead schedule screens, "
            "conference furniture and ash-black footprints, dim red emergency lighting, biomedical corporate interior, unsettling but realistic"
        ),
    },
    {
        "name": "Security Hollow",
        "slug": "security-hollow",
        "seed": 11023,
        "prompt": (
            "realistic cinematic image, Kallisto security worker in a fitted vest and suit shirt, partially ruptured but still holding a doorway by reflex, "
            "scanner strap clenched in one hand, squared shoulders, hard stuttering posture, modern research facility corridor, "
            "red emergency light, glass access doors, grounded body horror, believable corporate security setting"
        ),
    },
    {
        "name": "Crawler",
        "slug": "crawler",
        "seed": 11024,
        "prompt": (
            "realistic horror still, human body collapsed into wrong geometry crawling low through a waiting area in a biomedical conference floor, "
            "knees and elbows bent too far, ribs close to polished floor, threading under chairs and side tables, "
            "fallen brochures and badge lanyards, dim red emergency lighting, tense and believable anatomy, no fantasy elements"
        ),
    },
    {
        "name": "Motor Lurcher",
        "slug": "motor-lurcher",
        "seed": 11025,
        "prompt": (
            "cinematic realistic image, altered test subject trapped in broken training patterns inside a Kallisto motor assessment room, "
            "mid-step freeze then violent lunge posture, tape marks on floor, timing lights, evaluation targets, torn clinical clothing, "
            "stop-start motion implied, dim red emergency lighting, grounded biomedical horror, realistic environment"
        ),
    },
    {
        "name": "Stimulus Snatcher",
        "slug": "stimulus-snatcher",
        "seed": 11026,
        "prompt": (
            "cinematic realistic horror photo, sensory-driven ruptured subject inside a lab test pod, pupils blown wide, fingers spread like feelers, "
            "head snapping toward a bright light source, motion sensors and monitor glow in the background, "
            "modern clinical research setting, harsh red emergency light mixed with white lab reflections, realistic anatomy, in-world"
        ),
    },
    {
        "name": "Cocooned Subject",
        "slug": "cocooned-subject",
        "seed": 11027,
        "prompt": (
            "realistic cinematic horror image, half-transitioned patient-like figure on a medical observation bed, wrapped in exam paper, blanket strips, tubing, "
            "joints starting to unseal, face almost peaceful until the body tension shows, nearby biomonitor, privacy curtain, supply cart, "
            "dim red emergency lights, believable biomedical room, grounded body horror"
        ),
    },
    {
        "name": "Vent-Torn Rupture",
        "slug": "vent-torn-rupture",
        "seed": 11028,
        "prompt": (
            "cinematic realistic horror still, violently altered staffer in torn lab coat or visitor blazer, chest convulsing around burst lungs, "
            "black particulate and blood venting with a hard exhale, corridor in a corporate biotech building, "
            "dead wall screens and scattered clipboards, dim red emergency light, thick dust in the air, brutal but grounded"
        ),
    },
    {
        "name": "Echo-Throat",
        "slug": "echo-throat",
        "seed": 11029,
        "prompt": (
            "realistic cinematic horror image, voice-warped rupture in a keynote or AV room, throat and jaw visibly damaged like torn speaker fabric, "
            "microphone stands, dead projector, stage edge, conference chairs, mouth open mid-phrase, "
            "red emergency lights and faint dust haze, modern biomedical event setting, grounded and unsettling"
        ),
    },
    {
        "name": "Glare Stalker",
        "slug": "glare-stalker",
        "seed": 11030,
        "prompt": (
            "cinematic realistic horror photo, visual predator moving through Kallisto's test floor using reflections, "
            "gaunt altered human figure seen between cracked monitor glass, mirror shards, lens trays, and badge-reader screens, "
            "lab optics and reflective surfaces everywhere, dim red emergency light, high-end biomedical research interior, believable and dangerous"
        ),
    },
    {
        "name": "Cue-Snap Subject",
        "slug": "cue-snap-subject",
        "seed": 11031,
        "prompt": (
            "realistic cinematic image, altered test subject frozen unnaturally still in a behavior room until a timer click triggers sudden motion, "
            "metronome light, relay box, prompt speaker, evaluation desk, body caught between stillness and violence, "
            "modern corporate lab interior, red emergency lighting, grounded biomedical horror"
        ),
    },
    {
        "name": "Transfer Brute",
        "slug": "transfer-brute",
        "seed": 11032,
        "prompt": (
            "cinematic realistic horror image, former courier or escort-chain worker transformed into a heavy grab-and-drag brute, "
            "transport straps, case handles, and equipment webbing fused into shoulders and forearms, "
            "medical transfer corridor with specimen cases and rolling carts, dim red emergency lights, corporate biotech setting, realistic body horror"
        ),
    },
]


def make_pipe(model_id: str) -> StableDiffusionXLPipeline:
    pipe = StableDiffusionXLPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True,
    )
    pipe.enable_model_cpu_offload()
    pipe.set_progress_bar_config(disable=False)
    return pipe


def render(pipe: StableDiffusionXLPipeline, item: dict, out_dir: Path, width: int, height: int, steps: int, guidance: float) -> Path:
    out_path = out_dir / f"{item['slug']}.webp"
    generator = torch.Generator("cuda").manual_seed(item["seed"])
    image = pipe(
        prompt=item["prompt"],
        negative_prompt=NEGATIVE_PROMPT,
        width=width,
        height=height,
        guidance_scale=guidance,
        num_inference_steps=steps,
        generator=generator,
    ).images[0]
    image.save(out_path, format="WEBP", quality=92, method=6)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate generic encounter art for HELIX.")
    parser.add_argument("--model", default=MODEL_ID)
    parser.add_argument("--out-dir", default="encounter-art")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=768)
    parser.add_argument("--steps", type=int, default=28)
    parser.add_argument("--guidance", type=float, default=6.0)
    parser.add_argument("--only", action="append", dest="only", default=[])
    args = parser.parse_args()

    selected = PROFILES
    if args.only:
        wanted = {name.lower() for name in args.only}
        selected = [item for item in PROFILES if item["name"].lower() in wanted or item["slug"] in wanted]
        if not selected:
            raise SystemExit("No matching encounter profiles for --only.")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pipe = make_pipe(args.model)
    for item in selected:
        print(f"Rendering {item['name']} -> {out_dir / (item['slug'] + '.webp')}")
        render(pipe, item, out_dir, args.width, args.height, args.steps, args.guidance)


if __name__ == "__main__":
    main()
