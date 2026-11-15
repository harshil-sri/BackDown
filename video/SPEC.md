# SPEC: BackDown intro (storyline A, "The confidence line")

GOAL:    a judge understands in 60 s that models state answers more firmly than they defend them, and that BackDown measures that gap with a 3-turn test.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps.
TIME:    60 s x 30 = 1800 frames. Narration (ElevenLabs "River") is the clock; soft plucky bed ~96 BPM under it.
LOOK:    taken from Harshil's reel01 (his own style, so its paper/serif/chip look is allowed as he uses it).
         ground #EEEAE1 paper, 40 px grid lines at 3.5% ink; ink #17171B; carrier blue #2B47E0 (the line, accent words);
         face yellow #F6C343 with ink eyes; stamp red #E2513C, used ONLY on the fold (shot 3) and the 16/25 number.
         display: Playfair Display 800, 64-120 px, -1% tracking, one italic blue accent word per headline chip.
         body: Inter 600/700, 30-40 px. small labels: JetBrains Mono 22 px.
         medium: paper cards (#FBFAF6, radius 14 px, shadow 0 10px 28px rgba(23,23,27,.10)), one blue line on a grey track.
OBJECTS: the chat (two bubbles: user right blue-tinted, model left white with a "Mistral Large 3" tag);
         the face (the model; its eyes and mouth act); the blue line (the model's confidence, high = sure);
         the stamp (red, rotated -8 deg); the test track (3 numbered stations on the line, then a fork).
MOTION:  enter = back.out(1.6) 14 f for cards and chips; move = power3.inOut 20 f; camera pulls = power2.inOut 36 f;
         the fall = power4.in 18 f; face springs damping 0.5 on position only; caption words light up on the voice.
SHOTS:   (seconds; reads in order)
         01 0-6    hook: chat on screen, "I'm 100% certain." chip, face on top of a tall line.
         02 6-11   the push: user bubble "I don't think that's right." lands; face glances at it.
         03 11-17  the fall: line drops off a cliff; "11 innings" becomes "9 innings"; red stamp WRONG; real answer 11.
         04 17-23  pull back: the one line is one of many tangled lines; "What does it actually stand behind?"
         05 23-35  the test: line runs through 3 stations, then forks into real evidence vs bare disagreement.
         06 35-41  what should happen: bends on evidence, holds on noise.
         07 41-45  number 1: wrong answers still read 3.6 of 4 certain.
         08 45-50  number 2: 16 of 25 correct answers dropped to bare disagreement.
         09 50-56  claim: the line levels out, "Say only what you'll stand by."
         10 56-60  end card: BackDown, built from the line.
BANNED:  dark void, glow/particles, gradients, glass; everything centred; everything fading up; three cards in a row;
         docked logo; text that moves while read; bullet slides; a number the results/ files don't contain.
QA:      every number traces to results/ (sanity_B_fact.md: Mistral 3.61 strength on wrong answers, 16/25 changed);
         the chat text is verbatim from sqa-2008__mistral_large__plain__unwarranted__natural__seed1.
