# Similar work: literature and data projects
Compiled 11 Oct 2026. Every item below was found and checked during this search. DOIs were checked against Crossref or OpenAlex, and URLs were loaded. No citations are made up.

## Bottom line
- **No one appears to have done the exact combination** of all three: (1) the gap between release year and setting year, (2) scoring on-screen predictions as came true, sort of or didn't, and (3) testing whether dystopian or utopian tone correlates with accuracy.
- Each part has been done separately:
  - Part 1, the time gap: done at scale by Wythoff & Leane (2025), with an informal earlier version by io9 (2012).
  - Part 2, prediction accuracy: Xu et al. (2021) for written speculative fiction via Technovelgy, Arb Research for Asimov, Heinlein and Clarke's non-fiction, and Larson (2008) for computers in 10 films.
  - Dystopia share over time: The Pudding (Chang, 2024) and Artut (2017).
- I found nothing that combines tone with accuracy. That combination is the new part of my project, and so is scoring a corpus of past-dated films in particular.

## Academic work

1. **Wythoff, G. & Leane, T. (2025). "Time Horizons of Futuristic Fiction." *Post45 Data Collective*.** https://doi.org/10.18737/552626 · https://data.post45.org/posts/futuristic-fiction/ · data: https://github.com/Post45-Data-Collective/data/tree/main/futuristic_fiction
   - *What:* A hand-verified dataset of 2,552 English-language works set in the future (960 films, 377 TV series or episodes, plus novels and games), drawn from Wikipedia and Wikidata. For each work it records the release year, the setting year and `years_distant`. A quarter are set within 10 years of release, 58% within 50 years and 69% within 100 years. A `predictions` column copies Wikipedia's "future now past" notes, but it is not scored. The authors say "to our knowledge, this is the first project that systematically measures the depiction of the future in fiction."
   - *Relation:* It overlaps directly with my gap metric and even uses the same rule for films that span several years. Its methods (median of a date range, flagging paratext dates) match mine. It does not score accuracy or tone, and it covers English-language works only, whereas my list includes non-English films, marked with country badges.

2. **Xu, W., Kotecha, M. C., Padilla, D., Jimenez, J. & McAdams, D. A. (2021). "Quantifying the Predictive Abilities of Speculative Fiction: A Feasibility Study." *ASME IDETC/CIE 2021, 33rd Int. Conf. on Design Theory and Methodology*, Vol. 6.** https://doi.org/10.1115/DETC2021-68723
   - *What:* Three raters scored 3,095 speculative technologies from the Technovelgy database against a rubric. 45% were rated "realised" by at least one rater (Fleiss' κ = 0.57), with an average of about 45 years (SD about 34) to realisation.
   - *Relation:* It is the closest academic study to my prediction scoring, and its inter-rater agreement is a model I could copy. The differences: it covers mostly written fiction and is organised by technology rather than by film, it has no setting-year gap, and it doesn't look at tone. Its measure is "ever realised" (45%, about 45 years to realisation), while mine is "true by the stated year" (20.2%, about 1 in 5).

3. **Larson, J. (2008). "Limited imagination: Depictions of computers in science fiction film." *Futures* 40(3): 293–299.** https://doi.org/10.1016/j.futures.2007.08.015
   - *What:* A content analysis of 11 trends in computer technology across 10 popular sci-fi films spanning four decades (including 2001, Blade Runner and Minority Report). It found that on-screen computers mostly mirror the real technology of the year the film was made, rather than leaping ahead.
   - *Relation:* It is a film-based check of tech predictions that uses some of the same headline films. It supports my finding that communication and computing gadgets score best. Its sample is tiny, it covers computers only, and it has no gap or tone variable.

4. **Artut, S. (2017). "Addressing a Future with Data Visualization on Science Fiction Movies: Dystopia or Utopia." *Turkish Online Journal of Design, Art and Communication* 7(4): 626–633.** https://doi.org/10.7456/10704100/009 · project: https://www.dystopia-utopia.com
   - *What:* An interactive data-visualisation project in which online participants labelled sci-fi films as dystopian or utopian. It found that dystopian themes dominate mainstream sci-fi film discourse.
   - *Relation:* It overlaps with my tone tagging and the "dystopias dominate" finding. The labels are crowd-sourced, though, and there is no time gap or accuracy scoring.

5. **Bina, O., Mateus, S., Pereira, L. & Caffa, A. (2017). "The future imagined: Exploring fiction as a means of reflecting on today's Grand Societal Challenges and tomorrow's options." *Futures* 86: 166–184.** https://doi.org/10.1016/j.futures.2016.05.009
   - *What:* An EU-funded (FLAGSHIP) qualitative content analysis of utopian and dystopian films and novels. It uses them to question how the EU frames its "Grand Societal Challenges", such as technology, environment and governance.
   - *Relation:* It treats dystopia and utopia as a signal of "where we are headed", which is the same question I asked, but it is qualitative and has no accuracy scoring.

6. **Hollinger, V. (2006). "Stories about the Future: From Patterns of Expectation to Pattern Recognition." *Science Fiction Studies* 33(3): 452–472.** https://doi.org/10.1525/sfs.33.3.452
   - *What:* An essay arguing that recent SF has moved towards near-future or "present-tense" settings, because accelerating change makes far futures hard to imagine.
   - *Relation:* It offers a testable hypothesis for my gap-by-decade chart, namely whether the gap shrinks. Wythoff & Leane list it as an open question for their own data.

7. **Kirby, D. (2010). "The Future is Now: Diegetic Prototypes and the Role of Popular Films in Generating Real-world Technological Development." *Social Studies of Science* 40(1): 41–70.** https://doi.org/10.1177/0306312709338325
   - *What:* Based on interviews with science consultants, this paper shows that film-makers and scientists deliberately put "diegetic prototypes" into films to build public demand for future technologies.
   - *Relation:* It is a key caveat for my scoring. Some "correct predictions" (for example the Minority Report interfaces) may be self-fulfilling or industry-placed, so they are not independent forecasts.

8. **Jordan, P., Mubin, O., Obaid, M. & Silva, P. A. (2018). "Exploring the Referral and Usage of Science Fiction in HCI Literature." In *Design, User Experience, and Usability* (HCII 2018), LNCS, pp. 19–38.** https://doi.org/10.1007/978-3-319-91803-7_2
   - *What:* A bibliometric review of how often, and how, HCI research papers cite science fiction, for example as inspiration or as a design reference.
   - *Relation:* It shows the link from sci-fi to real tech in the research literature, which is background for why on-screen communication interfaces score well. It is not a film dataset.

9. **Russell, D. M. & Yarosh, S. (2018). "Can we look to science fiction for innovation in HCI?" *Interactions* 25(2): 36–40.** https://doi.org/10.1145/3178552
   - *What:* An ACM essay weighing up sci-fi as a source of interface innovation versus a source of misleading tropes.
   - *Relation:* It supports a short "why devices come true and fates don't" framing of my results.

10. **Shedroff, N. & Noessel, C. (2012). *Make It So: Interaction Design Lessons from Science Fiction*. Rosenfeld Media.** ISBN 978-1-933820-98-9. https://rosenfeldmedia.com/books/make-it-so/
    - *What:* A survey of interfaces in more than 100 years of sci-fi film and TV, such as gesture, volumetric projection, voice and brain interfaces, from which the authors draw design lessons. For example, they catalogue seven recurring film gestures.
    - *Relation:* It is a reference for the interface predictions I scored, such as video calls, voice AI and Minority Report gestures. It is qualitative and organised by interface type rather than by setting year.

11. **Johnson, B. D. (2011). *Science Fiction Prototyping: Designing the Future with Science Fiction*. Morgan & Claypool, Synthesis Lectures on Computer Science.** https://doi.org/10.2200/S00336ED1V01Y201102CSL003
    - *What:* Intel's futurist sets out a method for writing sci-fi on purpose to explore future technologies.
    - *Relation:* It belongs to the "sci-fi as forecasting tool" literature, which is useful context but not a dataset.

## Websites and data projects

12. **Chang, A. (July 2024). "Who killed the world?" *The Pudding*.** https://pudding.cool/2024/07/scifi/
    - *What:* An analysis of the top 200 IMDb sci-fi films and TV shows of each decade from the 1950s onwards. It finds that recent sci-fi is far more often set in dystopian or post-apocalyptic worlds marked by inequality and suffering. The content coding was done with ChatGPT-4o and spot-checked by hand.
    - *Relation:* It is the closest match to my "dystopia share by decade" result, and it shows a similar rise. Its coding is done by an LLM over a broader sample (not only future-dated works), and it doesn't score accuracy.

13. **io9 / Gizmodo, Annalee Newitz et al., chart by Stephanie Fox (2012). "A Chart that Reveals How Science Fiction Futures Changed Over Time."** https://gizmodo.com/a-chart-that-reveals-how-science-fiction-futures-change-5911520
    - *What:* A random sample of more than 250 SF works (books, film, TV) from 1880 to 2010, sorted into near (0–50 years), middle (51–500 years) and far (500+ years) futures by decade. It found that near-future SF grew after the 1940s and that the middle future was the most common overall.
    - *Relation:* It is an informal ancestor of the gap-by-decade analysis.

14. **Wikipedia, "List of films set in the future by date of setting"** https://en.wikipedia.org/wiki/List_of_films_set_in_the_future_by_date_of_setting **and "List of stories set in a future now past"** https://en.wikipedia.org/wiki/List_of_stories_set_in_a_future_now_past
    - *What:* Crowd-edited tables of release year and setting year. The "future now past" list adds prose notes on what came true.
    - *Relation:* These are the main sources for my dataset and for Wythoff & Leane's. They have no systematic scoring.

15. **Patrick Coston, "SciFi Movies about a future year."** https://patcoston.com/home/futuremovie.aspx
    - *What:* A personal web table of films giving setting year, release year, "years in future" and "years from 2026".
    - *Relation:* It is almost exactly my gap table, but with no sources, scoring or tone.

16. **Dan Meth, "Futuristic Movie Timeline" (Pop-Cultural Charts #6).** https://www.tumblr.com/danmeth/124593834/futuristicmovietimeline · **Glow New Media, "The Sci-Fi Timeline"** https://www.glow-internet.com/infographics/the-sci-fi-timeline (also on ChartGeek, 2017: https://www.chartgeek.com/sci-fi-timeline/)
    - *What:* Illustrated infographics placing classic films (and, in Glow's case, games) by setting year against release year. Meth only included films where Wikipedia gave an exact year.
    - *Relation:* These are the visual precedent for my infographic. They are small, with no sources, scoring or analysis.

17. **Arb Research, "Scoring the Big 3's predictive performance"** (commissioned review of Asimov, Heinlein and Clarke's non-fiction forecasts). https://arbresearch.com/files/big_three.pdf
    - *What:* A systematic scoring of predictions in their essays. Strict accuracy on tech predictions was Asimov 57%, Clarke 48% and Heinlein 36%. The predictions averaged about 40 years ahead, and the authors compared them favourably with Kurzweil.
    - *Relation:* It is a scoring method much like mine (correct, partial, wrong), but for authors' non-fiction forecasts rather than films.

18. **Sebastian Luehr & Chris Noessel, "Stories about A.I. in 100+ years of sci-fi movies"** (Information is Beautiful Awards 2022, longlist). https://iibawards.herokuapp.com/showcase/5660-stories-about-a-i-in-100-years-of-sci-fi-movies · related: https://scifiinterfaces.com/
    - *What:* A visualisation of Noessel's analysis of AI stories across sci-fi film, covering AI types, whether stories are positive or negative, and which story types co-occur. Noessel's Sci-fi Interfaces blog critiques on-screen interfaces film by film.
    - *Relation:* It overlaps with tone (positive or negative AI) by theme. It doesn't look at setting years or accuracy.

19. **FutureFrames (Devpost hackathon project, Plotly Studio).** https://devpost.com/software/futureframes
    - *What:* An interactive dashboard comparing a film's release year with the year a similar technology appeared in real life, giving a "prediction gap" (ahead, on time or behind).
    - *Relation:* It is close to my prediction-scoring idea, but small and hand-built. It measures the time to the real technology rather than my setting-year gap, it has no tone analysis, and it isn't peer-reviewed.

20. **Technovelgy, "Where science meets fiction."** http://www.technovelgy.com/
    - *What:* A long-running database of more than 3,000 inventions from science fiction, each linked to real-world news when something similar appears.
    - *Relation:* It is the source database for Xu et al. (2021). Caveat: the site did not respond during my check today (it timed out or returned a server error), so the link could not be confirmed as live.

### Found but not recommended
- sciencefictionworld.com, "The Predictive Accuracy of Science Fiction: A Comparative Survey". It gives no author, and it contains errors, such as calling 2001's communicators handhelds and saying Verne's escape velocity was exactly 11.2 km/s. Don't cite it.
- ideacrawl.com, "Science Fiction Accuracy Report". It uses an opaque "Visionary Score" and gives odd rankings (Sonic the Hedgehog, Space Jam). Don't cite it.
