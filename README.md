# Sum up 23 November's world news in one image

Entry for the make.fun bounty
[`news-image-20261123`](https://make.fun/bounty/news-image-20261123)
($100, top 50 entries share it; deadline 25 Nov 2026, 00:00 UTC).

## The image

`entry.png` (1024×1024, ~140 KB) is a newspaper front page,
**"The World in One Page — Monday 23 November 2026"**, built from the real
headlines of that day. Lead story: **COP31 collapses with no climate deal**
(Antalya — fossil-fuel language stripped, EU and island states refuse to
sign). Six more stories: Trump says the 28-point Ukraine peace plan is
"not my final offer" (Kyiv has until 27 Nov; Kushner floats NATO-style
guarantees); 15 killed near Kyiv and Ukraine sinks a Russian corvette off
Libya; Nvidia reinstates Jensen Huang as CEO after Trump pressure; the US
imposes sweeping new sanctions on Iran as Tehran vows to counter any Hormuz
blockade; a factory fire in Indonesia kills at least 24 (~30 missing); Modi
offers Nepal NPR 24,000 crore in aid with 8 MoUs and a new
Ayodhya–Janakpur train. "Also today": Democrats' largest US House majority
since 1992 (258 seats), FIFA awarding the 2031 Women's World Cup to the
USA/Mexico/Costa Rica/Jamaica, BepiColombo reaching Mercury, and the disputed
AI "proof" of the Riemann hypothesis.

Headlines were researched on 24 Nov 2026 from that day's reporting
(BBC, Reuters, CNN, AP, AFP, and day-recaps such as Principia's
23 Nov 2026 edition).

## How it is built

`build_image.py` renders the poster with Pillow (DejaVu fonts) — no network,
no randomness, no timestamps, so re-running it writes byte-identical output.
`main.py` (Python 3.13, standard library only) copies the committed
`entry.png` to `/output/entry.png` byte-identically on every run, which is
the entrypoint the grader runs (no network at run time).

## Verify

```sh
python3 build_image.py            # regenerates entry.png deterministically
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 -c "from PIL import Image; im = Image.open('out/entry.png'); print(im.size, im.format)"
```

## License

MIT — see `LICENSE`.
