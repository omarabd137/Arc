# ARC: Narrator Voice, Topics & Trends, Packaging & Launch (research notes, 05.11.2026)

Note: vidIQ and TubeAlfred tools were not used, as instructed. The only YouTube data tool available here routes through TubeAlfred, so channel-level view counts for most reference channels could not be pulled and are listed under Gaps. Tags: [observed] = stated in a source; [estimated] = my inference or a vendor estimate.

## A) Narrator voice: qualities, WPM, ElevenLabs voices, settings, licensing

### Takeaway
For a calm documentary feel, aim for about 130–145 WPM, not the roughly 165 WPM that TTS tools tend to default to (a likely reason Jason sounded hectic). On ElevenLabs, the strongest current default candidates for warm, calm narration are Brian (deep, resonant, American), George (warm, British), Daniel (authoritative, British, news-style) and Bill (friendly storyteller). ElevenLabs now recommends Eleven v4 over v3. A paid plan is needed for monetized use.

### Cited Findings
- [observed] Documentary narration pace: about 130–145 WPM; above about 160 "stops reading as documentary" and reads as an explainer. Explainer/e-learning pace: about 140–160 WPM. Slow documentary/meditation pace: about 110–130 WPM. 150 WPM is a common rule of thumb. — [voxbooster](https://voxbooster.com/blog/ai-voice-generator-documentary-voiceover); [narrationbox](https://narrationbox.com/blog/how-to-control-pacing-pauses-emotion-ai-voiceover); [wordtotime](https://wordtotime-org.pages.dev/blog/voice-over-rates-and-timing). These are vendor blogs, not studies.
- [observed] "Most TTS defaults sit near 165" WPM, so a default-settings render may run too fast for documentary. A vendor sample of 53 long-form voiceovers had a median of 166.5 WPM (anecdotal). — [search summary of voiceover pace sources](https://voxbooster.com/blog/ai-voice-generator-documentary-voiceover); [overseeros](https://www.overseeros.com/blog/youtube-script-length-word-count)
- [observed] ElevenLabs speed setting: default 1.0, minimum 0.7, maximum 1.2; "Extreme values may affect the quality." — [ElevenLabs TTS best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [observed] ElevenLabs model guidance: "We strongly recommend switching to v4 and testing it with your own voices and content." Eleven v3 and v4 do not support SSML `<break>` tags; use audio tags, ellipses and text structure for pauses. Multilingual v2 is better at reading out numbers ("a larger model"), which matters for finance scripts. Older models support `<break time="x.xs"/>` up to 3 s, but too many cause instability. "The pacing of the audio is highly influenced by the audio used to create the voice." — [ElevenLabs TTS best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [observed] Stability: lower values widen emotional range and higher values make the tone more consistent. Style amplifies the speaker's style and may add latency. — [Runware v3 schema](https://runware.ai/docs/models/elevenlabs-v3/schema.json); [ElevenLabs voice settings API](https://elevenlabs.io/docs/ko/api-reference/voices/settings/get.md)
- [observed, secondhand] Narration settings cited by third parties: defaults are stability 0.50, similarity 0.75, style 0. An SDK example uses stability 0.85 for "clear, consistent narration" and 0.45 for expressive dialogue. Another guide uses 15–35% stability for emotional fiction. — [mintlify ElevenLabs python mirror](https://www.mintlify.com/elevenlabs/elevenlabs-python/api-reference/voices/settings); [aiproductivity guide](https://aiproductivity.ai/guides/elevenlabs-audio-quality-optimization/); [openskillindex](https://openskillindex.com/skills/comeonoliver-skillshub-elevenlabs-core-workflow-a)
- [observed] Default voice IDs and descriptors (third-party list; cross-check in the dashboard):
  - Brian `nPczCjzI2devNBz1zQrb`: middle-aged, "resonant, comforting", narration
  - George `JBFqnCBsd6RMkjVDRZzb`: "warm, captivating", narration
  - Daniel `onwK4e9ZLuTAKqWW03F9`: "strong, authoritative", broadcast/news
  - Bill `pqHfZKP75CvOlQylNhV4`: "friendly, comforting", storytelling
  - Adam `pNInz6obpgDQGcFmaJgB`: "bright tenor, brash and confident" (less calm)
  - Chris `iP95p4xoKVk53GoZ742B`: natural, down-to-earth
  - Eric `cjVigY5qzO86Huf0OWal`: smooth tenor, 40s
  - Roger `CwhRBWXzGAHq8TQ4Fs17`: easygoing
  - Will `bIHbv24MWmeRgasZH58o`: laid back
  - Callum `N2lVS1w4EtoT3dr4eOWO`: gravelly
  - Liam `TX3LPaxmHKxFdv7VOQHJ`: energetic, for reels
  - Charlie `IKne3meq5aSn9XLyUdCD`: Australian, energetic

  — [WaveSpeed ElevenLabs voice ID list](https://wavespeed.ai/docs-api/elevenlabs/elevenlabs-voice-id). The same IDs for Brian, Daniel and George appear in a Blotato table (Brian: "American, deep, narration"; Daniel: "British, authoritative"; George: "warm, British"). — [Blotato via search](https://help.blotato.com/api/accounts/voice-ids). One source (Voximplant) calls Daniel "American, casual", which conflicts. — [Voximplant](https://voximplant.com/docs/references/voxengine/voicelist/elevenlabs)
- [observed] ElevenLabs "Documentary narrator voices" library page features: "Dan – Engaging Science Instructor" (British, warm, recommended for YouTube/explainers) `BHr135B5EUBtaWheVj8S`; "Patrick International" (deep, documentary) `9Ft9sm9dzvprPILZmLJl`; "Bill – Informative, Clean and Natural" (American) `lnUnPeUhSI5EcqtFBux7` (a library voice, not the default Bill); and "Grandma Rachel" `0rEo3eAjssGDUCXHYENf`. No usage stats are shown. — [ElevenLabs voice library: documentary narrator voices](https://elevenlabs.io/voice-library/documentary-narrator-voices)
- [observed] Legacy default voices were deprecated (original date 28 Feb 2026) and are now "fully deprecated and removed from all products". API calls to legacy IDs auto-route to replacements, e.g. Antoni/Arnold→Adam, Josh/Jeremy→Craig, Michael→Robert, Patrick→Lawrence, Thomas/Ethan→Tom, Dave→Geoffrey, Joseph→Goliath. Brian, Daniel, George, Bill, Chris, Eric, Callum, Roger, Will, Liam and Charlie are **not** on the legacy list. — [ElevenLabs: What are Legacy voices](https://elevenlabs.io/docs/help-center/product/voices/my-voices/what-are-legacy-voices.md); [Vapi legacy migration](https://docs.vapi.ai/providers/voice/vapi-voices/legacy-migration)
- [observed, unverified] One blog claims all Default voices expire 31 Dec 2026 and that accounts created after March 2026 cannot access them. I found no official confirmation. — [cognitivefuture](https://cognitivefuture.ai/?p=4844)
- [observed] Licensing: the free plan "does not include a commercial license". Starter ($5/mo) is the cheapest tier with commercial rights. Audio generated while subscribed stays usable after downgrading. Cloned voices need appropriate permission even on paid plans. — [ElevenLabs: Can I publish the content I generate](https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform.md); [bigvu pricing 2026](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/); [terms.law](https://terms.law/ai-output-rights/elevenlabs/)

### Inferences
- [estimated] Jason Steele most likely felt pushy because of a fast default rate combined with an expressive (low-stability) voice. Fix both: target about 135–145 WPM (speed about 0.9–0.95 or slower script pacing, plus ellipses and paragraph breaks) and stability about 0.55–0.75, style 0–0.15, similarity about 0.75.
- [estimated] A shortlist to audition with one identical 60-second finance script: Brian (US, deep, calm, best fit for a US audience), George (British, warm, Kurzgesagt-like storyteller), Daniel (British authority), Bill (default), plus library voices "Dan" and "Patrick International". Test on Eleven v4 and on Multilingual v2, since v2 handles numbers better.
- [estimated] Default (ElevenLabs-owned) voices carry less licensing risk than community library voices, which matters given ARC's open voice-licence issue (memory: Short #01).

### Gaps
- No primary measurement of Kurzgesagt or Crayon Capital WPM; the 120–150 range in the brief is unverified.
- No official ElevenLabs page found listing current default voices with IDs; the IDs above come from third parties and need checking in the dashboard or `GET /v1/voices`.
- The terms for using community voice-library voices commercially were not confirmed.
- No official recommended stability/style values for v4 long-form narration.

## B) Topics & trends (finance/business/economics)

### Takeaway
Hard view-count evidence I could gather is thin. MagnatesMedia's top video is a crime/illegal-business story (Silk Road, about 6M views), and Folding Ideas' "Line Goes Up" (NFT critique) reached about 18M, which supports the scam/fraud and rise-and-fall angles. 2025 US search trends were dominated by policy-money topics (One Big Beautiful Bill Act, government shutdown, tariffs) and AI (DeepSeek). Finance RPM benchmarks cluster around $10–30 in the US, with insurance and tax at the top.

### Cited Findings
- [observed] MagnatesMedia: most-viewed video "The Most Illegal Business In The World: Silk Road" (26 Aug 2022), about 6.05M views. Channel totals: about 194.6M views, about 1.86M subscribers, 255 videos (Nov 2026). An older wiki lists "How WhatsApp Makes Money" as the most viewed. The creator cites a Rockefeller video with more than 6M views. — [vidIQ stats page (web page, not tool)](https://vidiq.com/youtube-stats/channel/@magnatesmedia/); [Social Blade](https://socialblade.com/youtube/handle/magnatesmedia); [YouTube Fandom wiki](https://youtube.fandom.com/wiki/MagnatesMedia); [magnatesmedia.com](https://magnatesmedia.com/)
- [observed] Folding Ideas' "Line Goes Up" (NFT/crypto critique) is the channel's most-viewed work; a snippet reports 18.3M views (film and date unconfirmed in the snippet). — [Wikipedia: Folding Ideas](https://en.wikipedia.org/wiki/Folding_Ideas)
- [observed] Google Year in Search 2025 (US trending, i.e. fastest growth, not volume): Charlie Kirk, KPop Demon Hunters, Labubu, iPhone 17, One Big Beautiful Bill Act, Zohran Mamdani, DeepSeek, Government shutdown… Tariffs were a major finance talking point. — [Search Engine Land](https://searchengineland.com/google-year-in-search-2025-trending-queries-465630); [Search Engine Journal](https://www.searchenginejournal.com/google-year-in-search-2025-gemini-deepseek-top-trending-lists/562440); [Webull](https://www.webull.ca/news-detail/13970640801866752)
- [observed] Finance RPM benchmarks (vendor blogs, 2026). US personal finance RPM: $15–40, $15–50 (average $28), or $12–28 depending on the FluxNote guide; OutlierKit gives $10–25 for finance; MilX gives RPM $5–20 with CPM $15–40. Insurance is the top sub-niche at $25–60 RPM. Tax content spikes seasonally and summer is softer. Several sources conflate CPM with RPM. — [FluxNote RPM by niche 2026](https://fluxnote.io/blog/youtube-rpm-by-niche-2026); [FluxNote US personal finance 2026](https://fluxnote.io/guides/youtube-rpm-personal-finance-us-2026); [FluxNote seasonality](https://fluxnote.io/guides/youtube-rpm-seasonality-finance-niche); [OutlierKit finance RPM](https://outlierkit.com/blog/youtube-rpm-finance-niche); [MilX](https://milx.app/trends/youtube-cpm-rpm-rates-2026-average-niches-countries-more); [Hubfluence CPM](https://www.hubfluence.io/resources/youtube-cpm-rates)

### Inferences
- [estimated] For ARC, the best-evidenced story formats are frauds/scams and illegal businesses (Silk Road, FTX, NFTs), billionaire/dynasty money stories (Rockefeller) and "how X makes money" company stories. Timely hooks for 2026 include tariffs, government debt and shutdowns, US tax-law changes and the AI bubble (DeepSeek moment).
- [estimated] An explainer-style channel (stories, not advice) will earn below pure personal-finance RPM. A realistic planning RPM is about $6–15 US-weighted, rising if topics touch tax, insurance, credit or investing keywords.

### Gaps
- No verified top-video view counts for Crayon Capital, ColdFusion, Economics Explained, Wendover, PolyMatter, Moconomy, Primal Space, Business Casual, Modern MBA or How Money Works. These searches returned nothing usable, and the only data tool available runs through TubeAlfred, which was excluded. Next step: sort each channel's /videos page by "Popular" manually.
- No 2026 Google Trends data for money topics (the 2026 Year in Search is not yet published; no finance category list found for 2025).
- No UK/CA/AU-specific RPM figures.
- No independent (non-vendor) RPM study.

## C) Packaging & launch (branding, cadence, Shorts, Test & Compare, inauthentic-content policy)

### Takeaway
YouTube's July 2025 "inauthentic content" update renamed "repetitious content" and targets mass-produced, templated videos, not AI-assisted original work. ARC is safe if every video has distinct scripting, narration and storytelling value. Test & Compare (up to three thumbnails, and now titles) picks the winner by watch-time share. An 18k-channel study supports a long-form-first mix with about 25–40% Shorts, and found gains in the business and education niches.

### Cited Findings
- [observed] The policy took effect 15 July 2025 and renamed "repetitious content" to "inauthentic content". It covers mass-produced or repetitive content, applies at channel level, and gives examples such as templated videos with minor variation and slideshows without narration or educational value. Creator Liaison Rene Ritchie called it a "minor update" for content that had been ineligible for years. AI tools are not banned. — [Gulf News](https://gulfnews.com/technology/youtube-updates-monetisation-policies-ai-and-repetitive-content-ban-begins-july-15-1.500192660); [Social Samosa](https://www.socialsamosa.com/news-2/youtube-clarifies-monetisation-policy-targeting-inauthentic-content-9493155); [PPC Land](https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/); [Plagiarism Today](https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/); [ContentGrip](https://www.contentgrip.com/youtube-tightens-monetisation/)
- [observed] Test & Compare: up to three thumbnail variants shown evenly; the winner is decided by watch-time share, which is distinct from average view duration. Title testing was added later (dated mid-2025, Dec 2025 or early 2026 depending on the source; up to three titles or combinations). Tests typically run about 10–14 days. — [ThumbnailTest news](https://thumbnailtest.com/news/youtube-releases-title-test-compare/); [PPC Land](https://ppc.land/youtube-expands-a-b-testing-to-include-titles-alongside-thumbnails/); [Toptal](https://www.toptal.com/creator/post/youtube-thumbnail-ab-testing); [Social Samosa](https://www.socialsamosa.com/news-2/youtube-thumbnail-testing-tool-more-creators-9498934)
- [observed] Shorts→long-form: in 2022, YouTube (Todd Beaupré) separated Shorts watch history from long-form recommendations so that Shorts viewing does not distort the long-form feed. — [vidIQ blog (article)](https://vidiq.com/blog/post/youtube-recommends-long-form-videos-shorts-viewers); [vidIQ blog](https://vidiq.com/blog/post/youtube-shorts-long-form-viewers-algorithm)
- [observed] AIR Media-Tech study: 18,000 English channels, Mar 2025–Mar 2026, 11 niches, correlational. Long+Short mix channels had more subscribers (median) in **business (+39%)**, **education (+37%)**, fitness (+41%) and food (+31%), mostly at small sizes. Gaming and entertainment favoured long-form only. Channels that pivoted their Shorts ratio by more than 30 points mid-year underperformed. Recommendation: Shorts at 25–40% of uploads (performance thins above 55%), roughly 1–2 Shorts/week alongside 3–5 long-form uploads, and change strategy gradually. — [AIR: Do Shorts help long-form? 18,000 channels](https://air.io/en/audience-growth/do-youtube-shorts-help-your-long-form-videos-grow-data-from-18000-channels)
- [observed] Third-party advice: keep a steady long-form schedule as the growth engine and add 3–5 Shorts/week if capacity allows. — [subscribr](https://subscribr.ai/youtube-strategy/youtube-shorts-for-long-form-growth-monetization)
- [observed] Disclosure: YouTube expects realistic synthetic content to be disclosed in some cases. — [gptprompts (secondary)](https://gptprompts.ai/elevenlabs-answers/can-i-use-elevenlabs-for-youtube-monetization)

### Inferences
- [estimated] Recommended ARC cadence: 1 long-form video every 1–2 weeks (quality over volume, since animation cost is high), plus 2–3 Shorts/week cut from each long-form video, each with a related-video link back to it. That keeps Shorts at about 30–40% of uploads, in line with the AIR figures.
- [estimated] Run Test & Compare on every long-form video, with three thumbnails and then titles, and judge by watch-time share, not CTR.
- [estimated] For inauthentic-content safety, vary structure, add original analysis and avoid template-identical intros and visuals across videos.

### Gaps
- No primary YouTube Help or Creator Insider page was fetched; the policy wording and Test & Compare details come from secondary coverage.
- No sourced best-practice data on faceless-channel branding (profile picture, banner, About text, trailer) or concrete examples from animated explainer channels. Searches were not completed within the tool budget.
- No official YouTube guidance on optimal upload frequency (YouTube generally does not prescribe one; not verified here).
