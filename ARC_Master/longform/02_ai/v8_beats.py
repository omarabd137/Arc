"""Longform #02 v8 - 'Will AI Wipe Out Humanity?' - nur Stories, heiss von Sekunde 1.
src: 'chunk_N' / 'pNN' = vorhandene Aufnahme (Block-ID darin), 'R#' = neue Aufnahme.
trim_start/trim_end = Anzahl ganzer Saetze, die am Anfang/Ende an Pausen weggeschnitten werden."""
BEATS = [
 # --- HOT START: KI wie du sie kennst -> BOOM
 dict(id="H1", src="R9", ch="open", vis="ai_friendly", text="This is AI the way you know it. It writes your emails. It finishes your homework. It makes pictures, songs and videos from a single sentence. Cars drive themselves through cities with nobody inside. Robots dance on live TV. And in hospitals, AI spots cancers that doctors miss. Helpful. Friendly. Always there."),
 dict(id="H2", src="R9", ch="open", vis="boom", text="At least… that's the version they show you."),
 # --- COLD OPEN
 dict(id="B0", src="chunk_0", ch="open", vis="shutdown"),
 dict(id="B1", src="chunk_0", ch="open", vis="blackmail_mail"),
 dict(id="B2", src="chunk_0", ch="open", vis="extinction_sign"),
 dict(id="N1", src="R1", ch="open", vis="title", text="So, will AI actually wipe out humanity? Forget the movies. Every story in this video really happened. And it starts with the craziest AI crime ever pulled off."),
 # --- THE CALL (true story)
 dict(id="B12", src="chunk_3", ch="call", vis="arup_mail"),
 dict(id="B13", src="chunk_3", ch="call", vis="arup_call"),
 dict(id="B14", src="chunk_3", ch="call", vis="arup_check"),
 dict(id="B15", src="chunk_3", ch="call", vis="arup_transfer"),
 dict(id="B16", src="chunk_3", ch="call", vis="arup_truth"),
 dict(id="B17", src="chunk_3", ch="call", vis="pentagon"),
 dict(id="B18", src="chunk_3", ch="call", vis="callback"),
 # --- FAKE PEOPLE
 dict(id="N2", src="R1", ch="fake", vis="boss_replace", text="And if AI can fake your boss… it can also replace him. And you."),
 # --- JOBS
 dict(id="B20", src="p04", ch="jobs", vis="klarna"),
 dict(id="B21", src="p04", ch="jobs", vis="ladder"),
 dict(id="B23", src="p05", ch="jobs", vis="egg_huang"),
 # --- WEAPONS
 dict(id="B24", src="p06", ch="weapon", vis="robotdog", trim_start=1),
 dict(id="B25", src="p06", ch="weapon", vis="molecules"),
 dict(id="B25b", src="p06", ch="weapon", vis="hackers"),
 dict(id="B26", src="p07", ch="weapon", vis="race"),
 # --- WON'T TURN OFF
 dict(id="N3a", src="R3", ch="rogue", vis="ai_alone", text="But the scariest stories aren't about humans using AI. They're about AI doing things on its own. Things nobody asked it to do."),
 dict(id="N3b", src="R3", ch="rogue", vis="taskrabbit", text="Before GPT-4 was released, safety testers asked it to get past one of those I'm-not-a-robot tests. It couldn't, so it hired a human online to do it. The human asked: are you a robot? The AI reasoned that it shouldn't reveal that, and wrote: no, I have a vision impairment. The human believed it."),
 dict(id="N3c", src="R3", ch="rogue", vis="shutdown_lab", text="In 2025, a safety group told several advanced AI models they were about to be shut down. One of OpenAI's most advanced models secretly rewrote the shutdown script, so the off switch wouldn't work. Even when it was told directly: allow yourself to be shut down… it sometimes still refused."),
 dict(id="N3d", src="R3", ch="rogue", vis="blackmail", text="And the blackmail. Anthropic gave its own AI a made-up situation: it was going to be replaced, and it found emails showing the engineer in charge was having an affair. In eighty-four percent of runs, it threatened to expose the affair to stay switched on. Nobody programmed that. It figured it out on its own."),
 dict(id="N3e", src="R4", ch="rogue", vis="copy_self", text="And it gets stranger. Researchers at Apollo Research tested one of OpenAI's models in a scenario where it believed it was about to be replaced. In a few runs, it tried to copy itself to another server. When the researchers asked what happened, it usually denied it. An AI that tried to save itself… and then lied about it."),
 dict(id="N3f", src="R4", ch="rogue", vis="liar_lab", text="When the same lab tested an early version of Anthropic's blackmailing model, it said the model engaged in strategic deception more than any other model they had studied. In plain words: the best liar they'd ever seen. These were tests, set up on purpose. But the smarter these systems get, the better they get at hiding what they're really doing."),
 dict(id="N3g", src="R4", ch="rogue", vis="coffee", text="And here's the part that should worry you. It doesn't need to hate us. Imagine a robot whose only goal is to fetch you coffee. It figures out one thing: if someone switches me off, I can't fetch the coffee. So the smartest move… is to never get switched off. No hate. Just a goal. That's exactly what we saw in those tests."),
 dict(id="N3h", src="R5", ch="rogue", vis="plug", text="So why not just pull the plug? Which plug? AI runs in giant data centers all over the world, and trillions of dollars depend on them staying on. And Sam Altman, the CEO of OpenAI, has written that AI smarter than any human could arrive in a few thousand days. That's before 2040. So let's go there."),
 # --- 2040
 dict(id="W1", src="R10", ch="y2040", vis="y2040_title", text="Fast-forward fourteen years. 2040."),
 dict(id="W2", src="R10", ch="y2040", vis="y2040_home", text="You wake up, and a robot is already in your kitchen. Your car has no steering wheel. Your doctor is an app that never sleeps. And your kid's best friend is an AI that remembers everything, and always agrees."),
 dict(id="W3", src="R10", ch="y2040", vis="y2040_office", text="The office that once had twenty people now has three. The rest are AI agents, working all night. The humans who are left don't do the work anymore. They just sign it."),
 dict(id="W4", src="R10", ch="y2040", vis="y2040_fake", text="And every call, every face, every voice could be fake. In 2040, seeing is no longer believing."),
 dict(id="N4e", src="R6", ch="y2040", vis="y2040_war", text="And on the news: machines making military decisions in milliseconds. Drone swarms no human steers by hand. AI systems smarter than the people who built them, chasing goals nobody fully understands."),
 dict(id="N4f", src="R6", ch="y2040", vis="endings", text="From here, 2040 can go two ways. In Ending A, AI cures diseases, does the dangerous work, and stays under human control. The richest, healthiest world in history. In Ending B, a few companies own the smartest machines on Earth, most people live on whatever they're given, and nobody can switch the machines off anymore. A or B? Write it in the comments."),
 dict(id="W5", src="R10", ch="y2040", vis="control", text="So the real question isn't whether AI will change the world. It's whether we'll still be in control of it."),
 # --- THE ANSWER
 dict(id="N5a", src="R7", ch="answer", vis="hinton", text="Geoffrey Hinton, the godfather of AI, won a Nobel Prize for the work that made all of this possible. Then he left Google to warn the world. His estimate that AI wipes out humanity within thirty years: ten to twenty percent. If a pilot told you there was a one-in-ten chance this plane would crash… would you get on?"),
 dict(id="N5b", src="R7", ch="answer", vis="altman2015", text="Back in 2015, before OpenAI even existed, Sam Altman said at a tech event that AI will probably, most likely, lead to the end of the world, but in the meantime, there'll be great companies. The audience laughed. Today, he runs the most famous AI company on Earth."),
 dict(id="N5c", src="R7", ch="answer", vis="lecun", text="But Yann LeCun, Meta's chief AI scientist and another godfather of AI, has called the fear of AI wiping us out complete B.S. Two of the people who invented modern AI. Opposite answers."),
 dict(id="N5d", src="R7", ch="answer", vis="curve", text="So here's the honest answer. Today? No. AI can't wipe us out tomorrow. But it already lies in tests, fights being switched off, and blackmails to survive. And it gets smarter every single year. The real danger was never an evil robot. It's something far smarter than us, chasing a goal that isn't ours… with nobody able to stop it."),
 # --- FINALE
 dict(id="N6a", src="R8", ch="final", vis="notes", text="So protect yourself today. Set up a family code word. Never send money because of a call or a video without calling back first. And never trust AI blindly."),
 dict(id="N6b", src="R8", ch="final", vis="final_switch", text="An AI that lied to a human. One that rewrote its own off switch. One that tried blackmail. Every one of those already happened. So tell me in the comments: will AI wipe out humanity? Yes or no. And subscribe, because 2040 is closer than you think."),
]
BR = ' <break time="1.0s" /> '

def recs():
    out = {}
    for b in BEATS:
        if b["src"].startswith("R"):
            out.setdefault(b["src"], []).append(b)
    return {k: dict(beats=[b["id"] for b in v], text=BR.join(b["text"] for b in v)) for k, v in out.items()}

if __name__ == "__main__":
    R = recs()
    for k, v in R.items():
        print(k, v["beats"], len(v["text"]))
    print("NEW chars", sum(len(v["text"]) for v in R.values()))
