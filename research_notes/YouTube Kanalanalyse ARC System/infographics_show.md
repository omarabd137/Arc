# The Infographics Show (@TheInfographicsShow): 360° channel and video system analysis

Research date: 05 Nov 2026. Channel ID: UCfdNM3NAhaBOXCafH7krzrA.

Method note: youtube.com web pages (/about, /videos, /community, /playlists) redirected to a Google consent wall (gl=DE). I did not accept it. Observed data comes from: (a) the official YouTube RSS feeds (uploads, long-form-only UULF and Shorts-only UUSH playlists), (b) watch-page player metadata (duration, description, captions list) for 4 recent videos, (c) i.ytimg.com thumbnails for 6 recent videos, which I inspected visually, and (d) third-party stat sites. Caption text could not be downloaded: the caption URLs returned 0 bytes, transcript sites returned 403, and an alternative route was refused as bot-check circumvention. So WPM, verbatim hooks and sponsor-read text are **gaps**. Social Blade returned 403 (only a search snippet is available). vidIQ/TubeAlfred were not used.

Tag legend: [observed] = I saw it directly in YouTube data or the thumbnails; [estimated] = third-party estimate or my inference.

## 1. Channel packaging (subs, videos, views, cadence, branding)

### Takeaway
The channel has about 15.5M subscribers, about 7B views and about 6.3K videos, and it currently publishes **two long-form videos a day**. Uploads are scheduled at fixed times: always at minute :11, around 02:11 UTC and 15:11–21:11 UTC. It is effectively a daily content factory that started in 2011.

### Cited Findings
- Channel creation date 2011-02-26 [observed]: shown in the uploads feed header — [YouTube RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCfdNM3NAhaBOXCafH7krzrA)
- 15.5M subscribers, 7.0B total views, 6.3K videos, ~1.1M average views/video, ~1.2M views/day lifetime, 97% long-form / 3% Shorts, ~9.1 videos/week (~39/month), recent average length ~38:40, country United States [estimated, third-party] — [OutlierKit](https://outlierkit.com/channel/theinfographicsshow)
- Social Blade snippet: "16M subscribers, 6.9B views, 6.3K videos", while its milestone bar shows 15.5M. vidIQ snippet: 15.5M subscribers, +100K in the last 30 days [estimated, search snippets only] — [Social Blade](https://socialblade.com/youtube/handle/theinfographicsshow/achievements); [vidIQ stats page](https://vidiq.com/youtube-stats/channel/@theinfographicsshow/) (snippet only, tool not used)
- ~8M subscribers as of April 2020 (from an article title cited on Wikipedia) [estimated] — [Wikipedia](https://en.wikipedia.org/wiki/The_Infographics_Show)
- Cadence: the last 15 long-form uploads span 29 Oct–5 Nov 2026, which is exactly 2 per day. All are published at HH:11 UTC, mostly ~01:11–02:11 and ~15:11–21:11 UTC (evening US Eastern + afternoon US) [observed] — [Long-form feed UULF](https://www.youtube.com/feeds/videos.xml?playlist_id=UULFfdNM3NAhaBOXCafH7krzrA)
- Description boilerplate (observed on every sampled video): "Narrated by: Josh Risser", "🔔 Don't forget to SUBSCRIBE! 🔔", "SUGGEST A TOPIC: https://bit.ly/suggest-an-infographics-video", "💬 Come chat with me: https://discord.gg/theinfoshow", TikTok and Facebook links, "📝 SOURCES: pastebin.com/…", and "All videos are based on publicly available information unless otherwise noted." [observed] — [watch page YVFA79OhlU0](https://www.youtube.com/watch?v=YVFA79OhlU0)
- Category is "Education" on every sampled video [observed] — [watch page W8Dl-TS9H2c](https://www.youtube.com/watch?v=W8Dl-TS9H2c)
- Founder/producer: Andrej Preston (Slovenian, earlier the founder of the Suprnova.org torrent site), who has produced the channel since 2011 [observed via secondary source]. Tubi spinoff listings say "Directed by: Andrej Preston". The brief's name "Erick Hickman" is **not supported** by any source I found — [Wikipedia](https://en.wikipedia.org/wiki/The_Infographics_Show); [Tubi](https://tubitv.com/series/300018595/the-infographics-show-science-nature)

### Inferences
- The fixed :11 timestamps point to Studio scheduling on a production calendar, not ad-hoc uploads.
- The "Suggest a topic" link and the Discord drive a community-sourced topic funnel. The pastebin source link and the "publicly available information" line act as a credibility and policy hedge.

### Gaps
- I could not see the banner, profile picture, About text, trailer, Community tab or playlists because of the consent wall. These need manual checking in a browser.

## 2. Content strategy: pillars, outliers, psychology, spinoffs

### Takeaway
The classic evergreen pillars are morbid curiosity about the body and death, military "minute by minute" stories, true crime, prison and "what if". In 2025–26 the channel added a dominant **trend-jacking pillar about the AI, macro-finance and Big Tech collapse**. That pillar now produces most of its recent outliers, which makes it a direct competitor to ARC's niche.

### Cited Findings
- All-time top videos [estimated, third-party]: "What Happens When You Die?" 27M (59.6× typical); "Russian Sleep Experiment – EXPLAINED" 22M; "How SEAL Team Took Down Osama bin Laden (Minute by Minute)" 20M; "What Happens to Your Body While You Are Having Sex?" 19M; "How They Caught Serial Killer Ted Bundy" 17M; "Insane Way El Chapo Escaped Prison" 15M; "What Does it Actually Feel Like to be Shot" 14M; "What The Last 24 Hours of Death Row Prisoner Look Like" 14M; "What If North Korea Launched a Nuclear Bomb (Minute by Minute)" 13M — [OutlierKit](https://outlierkit.com/channel/theinfographicsshow)
- Recent outliers (≥1.5× recent median) [estimated]: "What if the AI Bubble Bursts (Day by Day)" 4.7M in 29 days (10.4×); "He started his new job at 7:30 AM. By 9:45 AM, he grounded America." 2.5M; "The Leaked Audit That Exposes OpenAI's Real Financial Crisis" 2.5M; "Leave Windows 11 Idle for 24 Hours and Watch What Happens" 2.3M; "World War 3 – Hour by Hour in the Suburbs" 2.2M; "South Korea is Collapsing Faster Than Any Nation in History" 1.8M; "The 7 Trillion AI Gamble Is Failing. Big Tech is TRAPPED Right NOW." 1.8M; "The Next Great Recession Isn't Housing... Its FAR Dumber." 1.6M; "Sam Altman is panicking..." 1.5M — [OutlierKit](https://outlierkit.com/channel/theinfographicsshow)
- Topic mix [estimated, third-party]: Trend-jacking 60% / Evergreen 40%. Clusters: AI & tech anxiety 30%, global economic/demographic collapse 25%, geopolitics/military 20%, disasters/true crime/mysteries 20%, space 15%, health/finance warnings 10% (these sum to 120%, so they are approximate) — [OutlierKit](https://outlierkit.com/channel/theinfographicsshow)
- Last 15 long-form uploads with views at 5 Nov 2026 [observed]: "Holy sh*t spacetime is fake..." 2.08M (5 days); "Wall Street is freaking out over OpenAI now..." 1.46M (5 days); "MIT looked at what AI actually killed and holy sh*t..." 929K (1 day); "Russia Closing 5 Hospital Due to PLAGUE OUTBREAK" 645K; "The 11% Interest Trap Just Hit Wall Street. Elite Portfolios Are PANICKING Right NOW." 595K; "Most Terrifying Financial Shift in the World Right Now" 592K; "Top 10 Insane Dark Web Conspiracies That Were Actually True All Along" 581K; "UNPLUG Your Smart TV NOW!" 495K; "How Are Americans Affording $500,000 Homes on Average Salaries?" 453K; "$40 Trillion Debt Passed. The American ECONOMY Is Collapsing." 373K; "World War 3 Protocol..." 325K; "Ex-Google Executive: AI is Ending Capitalism" 314K (<1 day); "50 Geography Facts That Are Fake (But You Believed Them)" 148K; "YOU vs Horror Movie Killers" compilation 95K — [Long-form feed](https://www.youtube.com/feeds/videos.xml?playlist_id=UULFfdNM3NAhaBOXCafH7krzrA)
- Of those 15, 9 are about finance, the economy or AI business (OpenAI, Wall Street, debt, interest, housing, AI jobs) [observed] — same source
- Spinoffs/syndication: Tubi carries "The Infographics Show: Science & Nature" and "Society & Culture" series ("Starring: Josh Risser, Directed by: Andrej Preston"). There is also a podcast feed (Audible/Chartable) [observed via listings] — [Tubi S&N](https://tubitv.com/series/300018595/the-infographics-show-science-nature); [Tubi S&C](https://tubitv.com/series/300018596/the-infographics-show-society-culture); [Audible podcast](https://www.audible.com.au/podcast/The-Infographics-Show-Podcast/episodes/B0DDN57H55)

### Inferences
- The psychology is fear, threat to *your* money or body, plus voyeurism ("what it feels like", "last 24 hours"). The new finance videos frame macro news as a personal threat ("could hit your 401(k)", "your power bill").
- Time-structure formats ("Minute by Minute", "Day by Day", "Hour by Hour") recur across eras and outlier tiers. They work as a retention device because the narration promises a countdown.
- Recent median for sampled long-form is ~450–500K views, against a 1.1M lifetime average. Finance and AI topics reach 1.5–4.7M, so the pivot looks data-driven [estimated].

### Gaps
- There is no verified list of the channel's own YouTube spinoff channels (for example sibling channels). Not found.

## 3. Script & storytelling

### Takeaway
The structure is visible in the descriptions. Each one has a 3-paragraph thesis with a twist line, followed by 8 chapters of about 1–2.5 minutes each. A short cold-open hook runs 28–38 seconds before chapter 1. Each chapter title is a self-contained mini-question ("How…", "Why…"), and the final chapter always widens the stakes to "you".

### Cited Findings
- Chapter structure for "MIT looked at what AI actually killed…" (12:56): 00:28 entry-level jobs → 01:37 MIT Iceberg Index → 02:43 senior vs graduates → 04:19 "$1.2 Trillion Wage Bill" → 04:58 "Rising Tide" → 07:14 → 09:17 → 11:28 "Massive Talent Shortage". The description's closing twist reads: "AI may not be destroying the corporate ladder, it may be removing the bottom rung." [observed] — [watch W8Dl-TS9H2c](https://www.youtube.com/watch?v=W8Dl-TS9H2c)
- "Wall Street is freaking out over OpenAI now..." (18:14) starts chapter 1 at 00:38. Chapters escalate to "How OpenAI's Risks Could Reach Your 401(k), Power Bill and Taxes" and "How an OpenAI IPO Could Pull Retirement Funds Into the Bet". The description uses hard numbers ("more than $13 Billion in revenue… operating costs reached roughly $34 Billion") and asks "So who ultimately pays for it?" [observed] — [watch M3hvIUwAL7c](https://www.youtube.com/watch?v=M3hvIUwAL7c)
- "The 11% Interest Trap…" (15:32) opens its description with "The rich aren't supposed to go broke like this." It explains "Buy, Borrow, Die" → margin calls → "How Forced Selling Can Hit Your 401(k)", and closes: "The wealthy may have signed the loans, but everyone can feel the fallout." [observed] — [watch YVFA79OhlU0](https://www.youtube.com/watch?v=YVFA79OhlU0)
- Second-person framing is a franchise: "YOU vs Xenomorph / Pennywise / Michael Myers…" compilation (1:56:18), described as testing "realistic tactical survival strategies" [observed] — [watch dg6bbyhFjhc](https://www.youtube.com/watch?v=dg6bbyhFjhc)
- Writers' room: a self-published profile of Yoshua Shelton says "Writer" 2018–2020, then "Lead Writer" 2020–2025, "1,300+ scripts", "3 to 5 scripts per week", led and mentored a writing staff, and worked with producers, animators and VO teams, with a military/defense specialty [estimated, self-reported] — [Twine profile](https://www.twine.net/yshelton)

### Inferences
- The template: cold-open hook (~30 s) → named authority or data source (MIT, a leaked audit, an ex-Google exec) → mechanism explained in plain language → escalating chapters → "how it reaches YOUR wallet" → reframing kicker line.
- Language level looks like plain US-English explainer prose (short sentences, dollar figures, everyday analogies), judging from the descriptions [estimated].

### Gaps
- I have no verbatim spoken hooks and no words-per-minute figure, because transcript download was blocked. Someone should pull captions manually (YouTube "Show transcript") for W8Dl-TS9H2c and M3hvIUwAL7c. The English track is a manual (uploaded) caption, so it would be accurate.

## 4. Visuals

### Takeaway
In the classic era the channel was known for flat 2D vector cartoon characters. The 2026 thumbnails, however, use a **detailed, painterly, semi-realistic cartoon caricature style** with recognizable real people (Einstein, a Putin likeness, a Wall Street executive figure) and dramatic lighting. This style is consistent with AI-assisted illustration [estimated].

### Cited Findings
- Six recent thumbnails, inspected visually [observed]:
  - "EINSTEIN WAS WRONG": a panicked Einstein with a shattering E=mc² on a purple background.
  - "THEY SOLD": a man pulling out empty pockets while a smirking investor stands behind him, with red "-85% / -72%" tickers.
  - "ZERO JOBS": a bulldozer pushing graduates in caps and gowns off a cliff.
  - "BLACKROCK BLEEDING": a sweating older executive locked in a pillory with a big red down arrow.
  - "IT'S STARTED": a Putin likeness wiping sweat while holding a biohazard folder in front of a red Kremlin.
  - "WORSE THAN YOU THINK": a worker fleeing a burning money printer.
  — thumbnails via [i.ytimg.com/vi/HTYIKPcPRRQ](https://i.ytimg.com/vi/HTYIKPcPRRQ/hqdefault.jpg), [M3hvIUwAL7c](https://i.ytimg.com/vi/M3hvIUwAL7c/hqdefault.jpg), [W8Dl-TS9H2c](https://i.ytimg.com/vi/W8Dl-TS9H2c/hqdefault.jpg), [YVFA79OhlU0](https://i.ytimg.com/vi/YVFA79OhlU0/hqdefault.jpg), [dnmdZOEGXe8](https://i.ytimg.com/vi/dnmdZOEGXe8/hqdefault.jpg), [eNzaPa9f0Ks](https://i.ytimg.com/vi/eNzaPa9f0Ks/hqdefault.jpg)
- A third-party write-up describes the format as "animated, voiceover-driven explainers with simple animation and heavy on-screen text". It is AI-assisted and unsourced, so weak evidence [estimated] — [AD HOC NEWS mirror](https://masukngab.pages.dev/news/ueberblick/the-infographics-show-and-the-business-behind-its-animated-explainers/69577231)
- The team includes animators and producers (from the writer's profile) [estimated] — [Twine](https://www.twine.net/yshelton). Wikipedia mirrors list Andrej Preston as "Motion Graphics Designer & Producer" [estimated] — per [search summary of Wikipedia mirror](https://kaweah.freedombox.rocks/kiwix/wikipedia_en_all_maxi_2023-10/The_Infographics_Show)

### Inferences
- The thumbnail style matches ARC's own target ("cartoon but realistic likeness"). The channel validates that this style can carry finance topics at scale.
- Whether the in-video animation also moved to the painterly style, or stayed flat-vector, is unverified.

### Gaps
- I have no frame-level data (visual changes per minute, speech bubbles, asset reuse), because no video frames were accessible. No job postings for animators were found, so outsourcing is unconfirmed.

## 5. Audio

### Takeaway
One recurring narrator, **Josh Risser**, is credited on every sampled video, and he has been made a brand face: a Short titled "Meet The Infographics Show Voice Over" got 1.09M views.

### Cited Findings
- "Narrated by: Josh Risser" appears in the descriptions [observed] — [watch YVFA79OhlU0](https://www.youtube.com/watch?v=YVFA79OhlU0)
- Short "Meet The Infographics Show Voice Over" (5 Oct 2024): 1,089,680 views [observed] — [Shorts feed](https://www.youtube.com/feeds/videos.xml?playlist_id=UUSHfdNM3NAhaBOXCafH7krzrA)
- Tubi spinoffs credit "Starring: Josh Risser" [observed] — [Tubi](https://tubitv.com/series/300018596/the-infographics-show-society-culture)
- The writer profile references a "VO team" and voice actors (plural) [estimated] — [Twine](https://www.twine.net/yshelton)

### Inferences
- A consistent human narrator is a brand asset and also a signal of authenticity under the YPP policy.

### Gaps
- Tone, pacing, WPM, music and SFX could not be assessed without audio or transcript access.

## 6. Shorts strategy

### Takeaway
Shorts are a minor, sporadic channel for The Infographics Show. They make up ~3% of content, and only a handful were posted in 2025–26, the latest on 1 Jun 2026. They are mostly cut-downs of evergreen body/death topics.

### Cited Findings
- Last 15 Shorts [observed]: "Stop Using Google RIGHT NOW" (Jun 2026) 108K; "Why Do You Have Pain Here When You Run?" (Jan 2026) 194K; "What Happens To Your Body When Smoking Weed" 270K; "What If You Jumped to the Center of the Earth" 234K; "What Happens When You Die" 176K (a repurposed top long-form topic); "What To ACTUALLY Do If You Are Buried Alive" 728K; "What Happens When You Are Shot" 2.98M (Nov 2024); "Meet The Infographics Show Voice Over" 1.09M; "Normal Day Jobs of Infamous Serial Killers" (Oct 2023) — [Shorts feed](https://www.youtube.com/feeds/videos.xml?playlist_id=UUSHfdNM3NAhaBOXCafH7krzrA)
- Format share: 97% long-form / 3% Shorts [estimated] — [OutlierKit](https://outlierkit.com/channel/theinfographicsshow)

### Inferences
- Shorts reuse proven long-form titles ("What Happens When You Die", "…Shot") and get 100K–3M views. Recently they are not used for the finance pillar.

### Gaps
- Looping and linking tactics (related-video links) could not be checked.

## 7. Thumbnails & titles

### Takeaway
Each thumbnail uses a 2–3 word all-caps verdict ("ZERO JOBS", "IT'S STARTED") above one panicked central character. The title supplies the specifics. The text and title never repeat each other.

### Cited Findings
- Thumbnail text, all sampled [observed]: EINSTEIN WAS WRONG / THEY SOLD / ZERO JOBS / BLACKROCK BLEEDING / IT'S STARTED / WORSE THAN YOU THINK. The text is white or magenta, heavy sans-serif with a dark outline/shadow at the top. Faces are in visible panic (sweat drops, wide eyes, open mouths). Visual cues include red down arrows, red % tickers, fire and money. The palettes are saturated red, purple or blue — [thumbnails](https://i.ytimg.com/vi/YVFA79OhlU0/hqdefault.jpg)
- Title-to-thumbnail pairing [observed]: title "Holy sh*t spacetime is fake..." pairs with "EINSTEIN WAS WRONG"; "Wall Street is freaking out over OpenAI now..." with "THEY SOLD"; "MIT looked at what AI actually killed and holy sh*t..." with "ZERO JOBS"; "The 11% Interest Trap… Elite Portfolios Are PANICKING Right NOW." with "BLACKROCK BLEEDING"; "Russia Closing 5 Hospital Due to PLAGUE OUTBREAK" with "IT'S STARTED"; "$40 Trillion Debt Passed. The American ECONOMY Is Collapsing." with "WORSE THAN YOU THINK" — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCfdNM3NAhaBOXCafH7krzrA)
- Title formulas observed in the 2026 uploads [observed]:
  - "[Authority] looked at X and holy sh*t..."
  - "[Entity] is freaking out / panicking..."
  - "[Number] [Thing] Just Hit Wall Street. [Group] Are PANICKING Right NOW."
  - "[Big $ number] … Is Collapsing."
  - "UNPLUG Your X NOW!"
  - "How Are Americans Affording…?"
  - "X Facts That Are Fake (But You Believed Them)"
  - "YOU vs …"
  - Classic: "What Happens When…", "What If… (Minute by Minute)", "How They Caught…"
  — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCfdNM3NAhaBOXCafH7krzrA); [OutlierKit](https://outlierkit.com/channel/theinfographicsshow)

### Inferences
- The channel has shifted from curiosity titles to alarmist, near-clickbait, ALL-CAPS urgency with casual profanity ("holy sh*t") and trailing ellipses. This is a creator-voice style that mimics individual finance YouTubers.

### Gaps
- No A/B (Test & Compare) data is available.

## 8. Descriptions / SEO

### Takeaway
Every description follows the same template: a 3-paragraph summary rich in keywords and numbers, 8 timestamped chapters with question-style keyword titles, a narrator credit, a subscribe CTA, a topic-suggestion link, Discord and socials, a pastebin sources link and a disclaimer. Player metadata shows **no tags** (keywords field empty).

### Cited Findings
- `keywords` = None on all 4 sampled videos; the English track is a manual caption plus about 20 auto-translated languages [observed] — [watch W8Dl-TS9H2c](https://www.youtube.com/watch?v=W8Dl-TS9H2c)
- Chapter titles are SEO phrases, for example "How Billionaires Use Stocks to Borrow Tax-Free Cash", "How Forced Selling Can Hit Your 401(k)" [observed] — [watch YVFA79OhlU0](https://www.youtube.com/watch?v=YVFA79OhlU0)

### Inferences
- Search value comes from chapters and descriptions, not from tags. The manual English captions help both accessibility and indexing.

### Gaps
- Pinned comments and end screens were not checked.

## 9. Monetization

### Takeaway
Revenue comes mainly from ads, through 13–18-minute videos (mid-roll eligible) plus 1–2-hour compilations, with off-platform syndication (Tubi, podcast). No sponsor link appeared in the 4 sampled 2026 descriptions. Revenue estimates are wide and unverified.

### Cited Findings
- Sampled durations [observed]: 12:56, 15:32 and 18:14 for the finance/AI videos, and 1:56:18 for the "YOU vs Horror" compilation. Recent average ~38:40 according to a third party, which compilations inflate — [watch pages](https://www.youtube.com/watch?v=M3hvIUwAL7c); [OutlierKit](https://outlierkit.com/channel/theinfographicsshow)
- Estimated monthly revenue $88K–$287K including sponsorship, with ad revenue $68K–$96K [estimated, third-party] — [OutlierKit](https://outlierkit.com/channel/theinfographicsshow). An unsourced "$11 million" net-worth claim exists [estimated, weak] — per [videoexplainers.com](https://videoexplainers.com/?p=2335)
- No sponsor links appear in the sampled descriptions. Historically there was a password-manager discount code, per a 2020 Medium post title [observed/estimated] — [Wikipedia citation list](https://en.wikipedia.org/wiki/The_Infographics_Show)
- Tubi FAST/AVOD series and a podcast feed exist [observed] — [Tubi](https://tubitv.com/series/300018595/the-infographics-show-science-nature)

### Inferences
- At 2 videos a day with a writing staff, producers, animators and VO, the team is likely in the dozens [estimated]. No public statement was found.

### Gaps
- Membership, merch shelf, team size and the founder's revenue statements were not found or not accessible.

## 10. Inauthentic / mass-produced content risk

### Takeaway
YouTube's 15 Jul 2025 update renamed "repetitious" content to "inauthentic content" and targets mass-produced, templated, low-variation videos. Enforcement can remove monetization from a whole channel. The Infographics Show stays safe through a credited human narrator, a staffed writers' room, unique per-video research with sources, and varied scripts.

### Cited Findings
- The policy is a rename of "repetitious content", effective 15 Jul 2025, per Creator Liaison Rene Ritchie; it is described as a clarification — [Search Engine Journal](https://www.searchenginejournal.com/youtube-monetization-update-spam-not-reaction-channels/550755/); [Gulf News](https://gulfnews.com/technology/youtube-updates-monetisation-policies-ai-and-repetitive-content-ban-begins-july-15-1.500192660)
- It applies at channel level: "monetization may be removed from your entire channel" — [ppc.land](https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/)
- AI tools are allowed when used to create authentic content; there is no exhaustive list of what counts as "mass-produced" — [Social Media Today](https://www.socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892/)

### Inferences
- Risk factors for a templated channel like ARC: identical structure plus synthetic voice plus reused assets plus no sources. Mitigations The Infographics Show demonstrates: a named narrator, a sources link, original research angles, and varied formats.
- Its alarmist finance titles ("Collapsing", "PANICKING") carry a separate misleading-metadata risk, and possibly lower advertiser suitability [estimated].

### Gaps
- I found no evidence that The Infographics Show itself has had YPP or policy problems.

## 11. What ARC should adopt / avoid

### Takeaway
**Adopt** the system: fixed cadence, chapter-driven scripts, a "how it hits YOUR money" escalation, a 2–3 word thumbnail verdict with a panicked caricature, a named consistent narrator, and sources in every description. **Avoid** copying its alarmist tone, its profanity-bait titles, and its daily volume without a team behind it.

### Cited Findings
- Finance and AI topics are now this channel's top performers (1.5–4.7M), which confirms demand and also means **direct competition** in ARC's niche — [OutlierKit](https://outlierkit.com/channel/theinfographicsshow); [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCfdNM3NAhaBOXCafH7krzrA)

### Inferences
- Adopt:
  1. A 12–18 minute length with about 8 timestamped chapters, each phrased as a "How/Why" keyword.
  2. A ~30 s cold open, then a named authority or data anchor (MIT, a leaked audit, $ figures).
  3. A final chapter that makes it personal: 401(k), power bill, taxes.
  4. A closing kicker line that reframes the topic ("removing the bottom rung").
  5. Thumbnails: 2–3 word caps verdict, one caricatured real figure in panic, red arrow or ticker, saturated single-hue background. Thumbnail text should complement the title, never repeat it.
  6. A narrator credit, a sources link, a "Suggest a topic" link and a disclaimer line in the description.
  7. Fixed publish slots for the US audience (~15:00–21:00 UTC).
  8. Time-structured formats ("Day by Day if X collapses").
- Avoid:
  1. Matching 2 videos a day: their volume rests on a multi-writer staff (3–5 scripts/week per writer).
  2. "holy sh*t" and fear-maximizing titles, which risk advertiser suitability and trust in a finance niche.
  3. Pure templating with no visible human authorship (inauthentic-content risk).
  4. Copying their thumbnail compositions one to one, which also aligns with ARC's own no-copy rule.
- Opportunity: The Infographics Show barely uses Shorts for finance, so ARC can own finance Shorts that feed its long-form videos.

### Gaps
- WPM, verbatim hooks, visual change rate, music and SFX all need manual transcript or frame review. Recommended videos: W8Dl-TS9H2c, M3hvIUwAL7c, and the outlier "What if the AI Bubble Bursts (Day by Day)" (ID not retrieved).
