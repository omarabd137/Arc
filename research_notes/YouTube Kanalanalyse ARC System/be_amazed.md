# BE AMAZED (@BeAmazed): channel and video system analysis for ARC

Research date: 05 Nov 2026. Method: public YouTube pages (About, Videos, Popular sort, Playlists, Home/Posts, three watch pages) read as logged-out HTML from a US/English locale, plus thumbnails from i.ytimg.com and third-party aggregators. No vidIQ or TubeAlfred tools were used.

Limits: the transcript endpoints returned nothing without a bot-check token, and I did not try to get around that. Transcript sites (youtubetotranscript.com, youtubetranscript.com) returned 403 or empty pages. Social Blade returned 403. So I could not quote spoken hooks or compute words per minute (see Gaps). [observed] = read directly from a page or file. [estimated] = my inference.

## 1. Channel packaging (subscribers, videos, views, cadence, banner, avatar, name, About, trailer, Community, playlists, owner)

### Takeaway
BE AMAZED is a mature UK-linked faceless channel. It has 13.5M subscribers, about 2,158 videos and 4.72B views. It currently posts about 2–3 long videos a week and no Shorts. Its packaging is minimal: a wordmark name, a generic About text, no trailer, a near-dormant Posts tab and a long tail of series playlists.

### Cited Findings
- [observed] About page: "13.5M subscribers", "4,717,700,275 views", "2,158 videos", "Joined Jul 22, 2015", channel ID UCkQO3QsgTpNTsOw6ujimT5Q, verified badge. — [YouTube About](https://www.youtube.com/@BeAmazed/about)
- [observed] Full About text: "Amazingly interesting bite-sized documentary-style fact videos. From most amazing people to future technology creations to facts about amazing mysteries — if it's amazing, we'll make a video on it. Oh, and there's a splash of humor thrown in too. You'll be amazed at our mind-blowing array of facts and condensed lists." The business contact is beamazed@lighthouseagents.com, a talent or management agency domain. The only external link is facebook.com/BeAmazedMedia. — [YouTube About](https://www.youtube.com/@BeAmazed/about)
- [observed] Channel keywords: "top 10" secrets most amazing "most amazing" incredible facts interesting technology documentary people creations mysteries beamazed "be amazed". — [YouTube About](https://www.youtube.com/@BeAmazed/about)
- [observed] Channel tabs (logged out, US): Home, Videos, Playlists, Posts, Store. There is **no Shorts tab and no Live tab**. — [YouTube channel](https://www.youtube.com/@BeAmazed)
- [observed] No channel trailer was found (no channelVideoPlayerRenderer on Home). The Home shelves are: Videos, Multiple playlists, All Our Videos, Popular videos, Posts. — [YouTube channel](https://www.youtube.com/@BeAmazed)
- [observed] Posts: only 4 posts are visible, all milestone or promo posts.
  - "Thank you all for 13 million subscribers!" (1 year ago, 9.4K likes). It promotes their card game "Nuh-Uh!" in the merch store.
  - A podcast launch post (3 years ago, 5.5K likes).
  - "10 MILLION SUBSCRIBERS!" (4 years ago, 41K likes). It is a humorous text that says "Behind the scenes we spend countless hours researching, fact-checking, writing, licensing, animating, illu[strating]…"
  - 9M subscribers (5 years ago, 11K likes).
  - The legacy /community URL shows "This Community isn't available". — [YouTube channel Home](https://www.youtube.com/@BeAmazed)
- [observed] Avatar: a default-style ytc avatar image. Banner: a 2560px image banner is present (yt3.googleusercontent.com/qli5bEDQ…). I did not inspect its visual content. — [YouTube channel](https://www.youtube.com/@BeAmazed)
- [observed] Playlists are evergreen series buckets. Examples with video counts:
  - Tales Of REVENGE! (18), Darwin Award Winners (19), Things You Will See For the First Time in Your Life (31)
  - The Most Expensive Things In The World (25), AMAZING HOUSES (23), Funniest Be Amazed Videos (71)
  - Secrets Hidden On Money (7), Most Expensive Mistakes (5), Genius People Who Beat The System (8)
  - Luckiest People Who Survived the Impossible (11), Survival Riddles (12), Gamers Caught Cheating (5)
  - EXPOSED (10), and All Our Videos (2,181). — [YouTube Playlists](https://www.youtube.com/@BeAmazed/playlists)
- [observed] Upload cadence: the 30 most recent uploads span about 3 months (oldest "3mo ago", newest "7d ago"), about 2.3 per week. — [YouTube Videos](https://www.youtube.com/@BeAmazed/videos). CreatorDB says "2.6 posts/week; last upload 2 days ago" (data from 1 Oct 2026). — [CreatorDB](https://creatordb.app/creatorstats/beamazed/)
- [observed] Recent publish times seen: 2026-10-25 12:00 PT and 2026-10-14 11:30 PT, which is midday US Pacific / evening UK. — [watch dmecXm59AdY](https://www.youtube.com/watch?v=dmecXm59AdY); [watch O9tgnCgfO_o](https://www.youtube.com/watch?v=O9tgnCgfO_o)
- Ownership and network:
  - A Roku listing names the developer "be amazed media ltd". — [Roku Guide](https://www.rokuguide.com/node/11491)
  - CreatorDB says the channel is UK-based and under the Lighthouse Agents network. — [CreatorDB](https://creatordb.app/creatorstats/beamazed/)
  - [observed] The footage licence paste is posted by user "beamazedmedia". — [Pastebin licences](https://pastebin.com/sDha7AGa)
- Growth stall and data conflict:
  - CreatorDB shows YouTube subscribers +0 over 30 and 90 days at 13.5M. CreatorDB itself flags this as possibly an artifact. — [CreatorDB](https://creatordb.app/creatorstats/beamazed/)
  - vidIQ (Aug 2025, via search snippet) listed about 13.3M subscribers, 4.79B views, 2,080 videos and an average length of 32 minutes. — [vidIQ stats page](https://vidiq.com/youtube-stats/channel/UCkQO3QsgTpNTsOw6ujimT5Q)
  - This conflicts with today's 4.72B public views. Either figure may be wrong, or views were removed through deletions or recounts. Also, +78 videos in about 15 months does not match about 2.3 uploads a week.

### Inferences
- [estimated] Subscriber growth has flattened (13.3M Aug 2025 → 13.5M Nov 2026, +0 per CreatorDB). The channel is in a "harvest" phase: views come from evergreen back-catalogue and recommendations, not subscriber growth.
- [estimated] "be amazed media ltd" plus a Lighthouse Agents contact point to a small UK production company with an agency handling sponsorships. It does not look like a large MCN.
- [estimated] Packaging investment (trailer, Posts, About) is low. All packaging effort goes into the thumbnail and title of each video.

### Gaps
- The visual content of the banner and avatar was not inspected. I found no official Companies House record or named staff or narrator.
- Social Blade (403) was unavailable, so there is no verified monthly view or earnings history.

## 2. Content strategy (pillars, outliers, why, audience psychology)

### Takeaway
The channel has moved away from "facts/secrets" lists (2016–2021) to "When X…" human-drama compilations (2024–2026): crime, cheating, karma, revenge and disasters caught on camera. Its all-time outliers are 25–30M-view evergreen curiosity topics. Those run about 50–70 times the current median of about 442K.

### Cited Findings
- [observed] Top all-time videos (Popular sort): Flight Secrets That Are Never Told To Passengers (30M, 4y, 24:39); Strangest Last Meal Requests On Death Row (30M, 6y, 11:16); Animals That Were SCARIER Than Dinosaurs (29M, 5y); Life Riddles You Must Solve To Stay Alive (26M, 8y, 11:33); Why Do Bees Die After Stinging? (25M, 4y); Secrets Of The Most Dangerous Magic Tricks Revealed (24M); Gamers Caught Cheating (21M); Craziest Soviet Machines You Won't Believe Exist – Part 1 (19M); Insane Theme Park Ride ACCIDENTS (19M); What Archaeological Sites Used To Actually Look Like (19M). — [YouTube Popular](https://www.youtube.com/@BeAmazed/videos)
- [observed] Money and business outliers: "From $42 Billion to $0 — How Anil Ambani Lost All His Money" (11M, 4y, 23:56); "Homeless People Who Won the Lottery" (12M, 9y); "Most Expensive Construction Mistakes In The World" (7.4M); "RICH People Who Turned Themselves into PLASTIC!" (7.5M); "Ads That LIE To Us" (7.3M). There are also playlists "The Most Expensive Things In The World" (25 videos) and "Secrets Hidden On Money" (7). — [YouTube Popular](https://www.youtube.com/@BeAmazed/videos); [Playlists](https://www.youtube.com/@BeAmazed/playlists)
- [observed] The 30 most recent uploads have median views of 442K, a mean of 566K, and a range of 140K–1.5M. The best recent ones:
  - "When They Don't Stop For Protesters" (1.5M, 3w)
  - "When Speedrunners Get Caught Cheating" (965K)
  - "The Smartest Moves In Horror Movies" (929K)
  - "Cringe Fake Rich Influencers Exposed as Poor" (909K, 10d)
  - "When Child Stars Go Off The Rails" (903K)

  The weakest were "Building Materials Vs Earthquakes" (140K) and "When Heroes Get Punished" (192K). — [YouTube Videos](https://www.youtube.com/@BeAmazed/videos)
- [observed] Recent title mix: 13 of 30 start with "When …" (e.g. "When Parents Find Out Their Kid Is The Killer", "When Thieves Rob The Wrong Store", "When Suspects Outsmart The Police"), and 4 start with "Watch …". — [YouTube Videos](https://www.youtube.com/@BeAmazed/videos)
- [observed] Franchises with numbered parts: Gamers Caught Cheating – Part 6, Darwin Awards [Part 5–9], The Power Of Time Parts 2–3, Luckiest People Who Survived The Impossible (Part 9), Passive Aggressive Ways People Got Revenge Part 1–3. — [YouTube Popular](https://www.youtube.com/@BeAmazed/videos)
- CreatorDB's FAQ (AI-assisted, unverified) says the audience is mostly over 35 and male-leaning. — [CreatorDB](https://creatordb.app/creatorstats/beamazed/)

### Inferences
- [estimated] Outlier drivers:
  - (a) A universal everyday context with a hidden layer: flights, bees, school, everyday things.
  - (b) Morbid curiosity: death row, deaths, killers.
  - (c) A "you'd never guess" reveal promise: secrets, revealed, "This Is What Happened Next".
  - (d) Evergreen topics with no news decay.
- [estimated] Psychology: curiosity gap plus mild schadenfreude/justice ("karma", "revenge", "caught cheating") plus awe ("biggest waves", "largest ships").
- [estimated] The recent "When…" drama pivot gets reliable 300K–1M results but has not produced new 10M+ outliers. Most 10M+ videos are 4–9 years old.
- [estimated] For ARC, the money items above show that finance "rise and fall" stories (Ambani $42B→$0) and "expensive mistakes" work inside a general-audience fact format.

### Gaps
- No view-velocity data, CTR or retention. The "vs median" ratios use lifetime views of old videos against recent videos, so they are biased toward old videos.

## 3. Script and storytelling (hooks, list structure, countdowns, teasers, loops, language, WPM)

### Takeaway
I could not retrieve transcripts, so no real openings can be quoted. Structure has to be inferred from titles, descriptions and the channel's own self-description.

### Cited Findings
- [observed] The channel describes itself as "bite-sized documentary-style fact videos… condensed lists" with "a splash of humor". — [YouTube About](https://www.youtube.com/@BeAmazed/about)
- [observed] The 10M-subscriber post shows the voice: jokey, self-deprecating, comparison-driven ("more people subscribed to this channel than there are flamingos in the world. Hah! Take that flamingos!"). It lists the workflow as "researching, fact-checking, writing, licensing, animating, illu[strating]". — [YouTube channel Home](https://www.youtube.com/@BeAmazed)
- [observed] Description hooks are one sentence and keyword-loaded. Examples:
  - "Fake rich influencers exposed! From rented Ferraris to fake private jets, these fake rich people exposed as broke will make you cringe."
  - "Tune in for some flight secrets that are never told to passengers!" — [watch dmecXm59AdY](https://www.youtube.com/watch?v=dmecXm59AdY); [watch RCyxK64uo6Q](https://www.youtube.com/watch?v=RCyxK64uo6Q)
- [observed] Tags on the top video show its item-list structure: "secret symbols on airplanes", "function of holes in airplane windows", "difference between first class economy and business class", "secret rooms in airplanes", "why airplane food tastes so bad", "boarding pass secrets". — [watch RCyxK64uo6Q](https://www.youtube.com/watch?v=RCyxK64uo6Q)
- [observed] None of the three sampled videos has chapters. — watch pages above
- [observed] Recent video lengths: median 37.0 min, mean 39.4 min, range 25.9–71.8 min. 2016–2018 videos ran 8–13 min. — [YouTube Videos](https://www.youtube.com/@BeAmazed/videos)

### Inferences
- [estimated] Structure: an unnumbered list of 10–20+ self-contained segments (the tags map one-to-one to segments). There are no chapters, which discourages skipping to the "best" item.
- [estimated] Moving from about 10 min to 25–70 min turns the "list" into a long-session, lean-back watch where each segment acts as a mini-hook.

### Gaps
- No verbatim openings, teaser lines, CTA wording or WPM. To fill this, pull a transcript manually (YouTube "Show transcript" in a browser) for RCyxK64uo6Q and dmecXm59AdY.

## 4. Visuals

### Takeaway
The channel uses licensed real footage and photos (stock plus viral-clip agencies), with its own animation and illustration on top. Recent thumbnails even mix a real photo with a cartoon illustration in one frame.

### Cited Findings
- [observed] Licence list in every description, quoted from the Pastebin "Licenses" page (Nov 2020):
  - Shutterstock as the primary image source, plus Creative Commons search.
  - ViralHog, Storyful, Newsflare, Jukin, Caters Clips, Alamy, Reuters and Getty for specific images.
  - VideoBlocks for background video. — [Pastebin licences](https://pastebin.com/sDha7AGa)
- [observed] The legal line reads "Unless otherwise created by BeAmazed, licenses have been obtained for images/footage in the video from the following sources". — [watch RCyxK64uo6Q](https://www.youtube.com/watch?v=RCyxK64uo6Q)
- [observed] The channel says it does "licensing, animating, illu[strating]" itself. — [YouTube channel Home](https://www.youtube.com/@BeAmazed)
- [observed] The recent title "When They Don't Stop For Protesters" (1.5M) is described as "a compilation of the tensest standoffs" and is tagged "protest compilation". — [watch O9tgnCgfO_o](https://www.youtube.com/watch?v=O9tgnCgfO_o)

### Inferences
- [estimated] The video body is mostly licensed viral or news clips (Newsflare, ViralHog, Jukin, Storyful) with narration and some overlays. Animation and illustration fill gaps where no footage exists.

### Gaps
- I did not see video frames, so cuts per minute, zoom use and overlays are unknown.

## 5. Audio

### Takeaway
This is unknown from public data. The channel is narrator-led with no on-camera host.

### Cited Findings
- A search summary describes it as a narration-driven, faceless channel with no publicly presented personalities. — [vidIQ stats page](https://vidiq.com/youtube-stats/channel/UCkQO3QsgTpNTsOw6ujimT5Q)

### Gaps
- Narrator identity, voice profile, music bed and SFX were not verifiable without watching or listening. Listen to 2 minutes of RCyxK64uo6Q.

## 6. Shorts strategy

### Takeaway
The channel has **no Shorts tab** (Nov 2026). It does not use YouTube Shorts as a growth lever.

### Cited Findings
- [observed] Tabs are only Home, Videos, Playlists, Posts and Store, and /@BeAmazed/shorts falls back to Home. — [YouTube channel](https://www.youtube.com/@BeAmazed)
- CreatorDB tracks linked Instagram and TikTok accounts (combined 13.8M followers including YouTube). Both are slightly declining: Instagram −633 and TikTok −606 over 90 days. — [CreatorDB](https://creatordb.app/creatorstats/beamazed/)

### Inferences
- [estimated] Their short-form activity happens off YouTube (IG/TikTok), possibly because licensed agency footage is restricted on Shorts. This is unverified.

## 7. Thumbnails and titles

### Takeaway
Thumbnails show one real-photo subject with a red arrow or circle zoom and a 1–3-word ALL-CAPS yellow or white caption. Recent ones add censored profanity or quote captions. Titles are plain-English curiosity statements with no numbers.

### Cited Findings (6 thumbnails inspected via i.ytimg.com/vi/<id>/hqdefault.jpg) [observed]
- **RCyxK64uo6Q** "Flight Secrets…" (30M): real airport-stairs photo, yellow top bar "ALWAYS BOARD LAST!", big red arrow pointing at the queue.
- **LNWYf0QXuVI** "Last Meal Requests" (30M): split frame with a mugshot on the left and a brick-like "meal" on a plate on the right. No text.
- **dmecXm59AdY** "Fake Rich Influencers": gold-bling car plus influencer, red circle magnifier on beads, yellow caption "PLASTIC!".
- **Q8EXdtk0Fu8** "Speedrunners Cheating" (965K): real streamer photo with a red dashed gaze line next to a **cartoon illustration** of the streamer and a red arrow. Yellow bar "SECRET MONITOR!".
- **O9tgnCgfO_o** "Protesters" (1.5M): aerial crowd with a tanker truck and sparks, white caption "f*cking move!".
- **njHFIOAwrDA** "Kid Is The Killer": real interrogation-room photo of a crying mother and son, quote caption "he f**ked the body".
- Source: [i.ytimg thumbnails](https://i.ytimg.com/vi/RCyxK64uo6Q/hqdefault.jpg)
- [observed] Title formulas:
  - "When [group] [does/gets X]" (13/30 recent)
  - "[Superlative adj] [things] [qualifier]" ("Dumbest Cave Deaths", "Worst Mating Rituals…")
  - "Secrets [X] Don't Want You To Know / Never Told To…"
  - "Why Do…?"
  - "[Specific story] – This Is What Happened Next"
  - "Part N" franchises
  - ALL-CAPS emphasis on one word ("CRAZIEST", "SCARIER", "ACCIDENTS")
  - Old 2016–17 titles used "Top 10…". — [YouTube Videos](https://www.youtube.com/@BeAmazed/videos)

### Inferences
- [estimated] The thumbnail text never repeats the title. It adds the payoff (title "Flight Secrets", thumbnail "ALWAYS BOARD LAST!"), which creates a second curiosity gap.
- [estimated] The profanity captions are a recent CTR lever with ad-suitability (yellow-icon) risk. ARC should not copy them.

## 8. Descriptions, SEO, tags

### Takeaway
Descriptions use a fixed template: a 1–2 sentence keyword hook, the same boilerplate links and a licence-credit line. Tags are now 20 long-tail keyword variants. There are no chapters or hashtags.

### Cited Findings
- [observed] Template:
  - Hook sentence
  - "Suggest a topic here to be turned into a video: http://bit.ly/2kwqhuh"
  - "Subscribe for more! ► …"
  - "Stay updated ► …"
  - "For copyright queries or general inquiries please get in touch: hello@beamazed.com"
  - "Merch: https://www.beamazed.store" (2026 videos)
  - "Legal Stuff." licence line plus Pastebin link. — [watch dmecXm59AdY](https://www.youtube.com/watch?v=dmecXm59AdY)
- [observed] 2026 tags are 20 close variants, e.g. for protesters: "protesters blocking road", "protesters blocking traffic", "road block protest" … "climate protesters blocking road". For fake rich: "fake rich influencers", "influencers exposed", "fake private jet", "instagram vs reality". The 2021 top video used brand tags ("beamazed", "be amazed", "top 10") plus item tags. — [watch O9tgnCgfO_o](https://www.youtube.com/watch?v=O9tgnCgfO_o); [watch RCyxK64uo6Q](https://www.youtube.com/watch?v=RCyxK64uo6Q)
- [observed] Category: Education, on all three sampled videos. — watch pages above
- [observed] Captions: the 2021 video has a manual English track plus auto-generated captions. The 2026 videos have only auto-generated (ASR) captions. — watch pages above

## 9. Monetization and policy risk

### Takeaway
Revenue comes from AdSense on 26–72-min videos, plus merch (Store tab, beamazed.store, "Nuh-Uh!" card game), a podcast, past game sponsorships and an agency for brand deals. The main risk is the reused and inauthentic-content rules for compilations built from licensed viral clips.

### Cited Findings
- [observed] 100% of the 30 recent videos are over 8 min (median 37 min), so mid-rolls are possible. A logged-out US player response showed only a pre-roll (AD_PLACEMENT_KIND_START) on two videos and none on the third. Mid-roll configuration cannot be seen from outside. — [watch dmecXm59AdY](https://www.youtube.com/watch?v=dmecXm59AdY)
- [observed] Merch store link and Store tab; the card game "Nuh-Uh!" was sold through the merch store (13M post). There is a podcast on all major platforms (post from 3 years ago). — [YouTube channel Home](https://www.youtube.com/@BeAmazed)
- Raid: Shadow Legends has sponsored the channel (search summary, date not given). — [vidIQ / search result](https://vidiq.com/youtube-stats/channel/UCkQO3QsgTpNTsOw6ujimT5Q)
- CreatorDB estimates the Instagram rate at $1.5K–$3.7K per post. It gives no YouTube estimate. — [CreatorDB](https://creatordb.app/creatorstats/beamazed/)
- On 15 Jul 2025 YouTube renamed "repetitious content" to "inauthentic content", covering mass-produced or repetitive content at channel level. Google said "There are no changes to our reused content policies which guide commentary, clips, compilation, and reaction content." — [SEJ](https://www.searchenginejournal.com/youtube-clarifies-monetization-update-targeting-spam-not-reaction-channels/550755/); [PPC Land](https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/); [YouTube Help](https://support.google.com/youtube/answer/1311392?hl=en)

### Inferences
- [estimated] BE AMAZED protects itself through paid licences (agency footage), original narration and commentary, and a public licence list. Its remaining risks are Content ID claims on agency clips and ad-suitability limits from crime or profanity thumbnails.
- [estimated] Long runtimes (37 min median) are a deliberate watch-time and mid-roll strategy.

## 10. What ARC should adopt or avoid

### Takeaway
ARC should adopt the packaging grammar, evergreen series and template SEO. It should not copy the clip-compilation body, profanity thumbnails or the drama/crime drift.

### Inferences [estimated, derived from findings above]
**Adopt:**
- Evergreen curiosity titles about universal contexts with a hidden layer, e.g. "Money Secrets Banks Never Tell Customers" modeled on "Flight Secrets…".
- Rise-and-fall money stories ($42B→$0 format, 11M views).
- "Most Expensive Mistakes" series and numbered "Part N" franchises with matching playlists.
- Thumbnails with one big subject, one red arrow or circle, and 1–3 ALL-CAPS words that add the payoff instead of repeating the title.
- Template descriptions with a keyword hook sentence, 15–20 long-tail tags, Education category and a sources line. ARC should list its own data sources the way BE AMAZED lists licences.
- A "suggest a topic" link for idea sourcing.
- Long formats (20–40 min) built from self-contained mini-segments.
- Mixing a realistic subject with a cartoon element, as in the SECRET MONITOR thumbnail. This fits ARC's cartoon-realistic style.

**Avoid:**
- Reused viral-clip compilations, which conflict with ARC's own 2D art and carry policy and Content ID risk.
- Profanity or crime-quote thumbnails (advertiser-unfriendly, against ARC's high-RPM goal).
- Neglecting Posts, Shorts and the trailer: the plateau at 13.5M suggests the missing Shorts funnel hurts new-audience growth.
- Titles with no finance angle drifting into true crime.

### Gaps
- No retention, CTR or RPM data. No verified transcript structure or voice profile. Verify manually before adopting script-level rules.
