<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Provide a thorough report on Xabi Alonso's tactical style, broken down per position/role. Do not stray away from using technical language. Discuss as if you are a UEFA Pro License Holder.

For each position/role, give a deep technical dive into what is expected of them, as well as what to strongly look for from a data analysis perspective.

Xabi Alonso’s game model is built around a 3‑4‑2‑1 that morphs into a 3‑2‑5 with a box midfield, asymmetrical wing-backs and aggressive, structured counter‑pressing, so every position is defined first by its contribution to central dominance and high regains rather than by traditional “lines.” Below is a role-by-role breakdown using coaching language and the key data lenses you’d use if you were auditing or profiling players for his system.[^1][^2][^3][^4][^5][^6]

***

## Game model overview

Alonso’s Leverkusen (and now Madrid) sides are possession‑dominant, using a 3‑4‑2‑1 that becomes 3‑2‑4‑1 or 3‑2‑5 in-possession, with a box of four in midfield, high wing‑backs and a lone 9 pinning the last line. The attacking play mixes positional ideas (fixed occupation of width and height) with relationist principles: short, close combinations and third‑man patterns in central and half‑space zones, rather than rigid “chalk on boots” spacing. Out of possession, his teams use an organised mid‑to‑high press and intense counter‑press; PPDA values around 10–11 vs ~12+ in prior seasons at Madrid illustrate the clear shift towards more aggressive ball‑recovery behaviour.[^7][^2][^3][^4][^5][^6][^8][^1]

From a data standpoint, you are trying to validate: (1) control of central zones (box midfield effectiveness, half‑space usage), (2) efficiency and volume of high regains and counter‑pressing, and (3) how well the 3‑2 rest‑defence behind the ball protects transition (field tilt, final‑third share spread almost evenly across left/centre/right: 33/34/33 for Leverkusen).[^3][^4][^5]

***

## Goalkeeper

Tactically, the goalkeeper is an auxiliary outfield player in the first line of build‑up, creating a 3+1 or even 4‑box‑2 structure against the opposition’s first line, and must be comfortable playing through or around a high press with disguised, firm passes into the pivot or wide centre‑backs. Because Alonso’s teams press high and hold a relatively advanced block, the keeper must also defend large spaces behind the back three, acting as an aggressive sweeper who anticipates depth runs and clears long balls before they become box entries.[^2][^5][^6][^8][^1]

Key metrics to monitor:

- Post‑shot xG minus goals (PSxG‑GA) and xGOT‑xG to assess pure shot‑stopping and shot quality management independent of the defence.[^9]
- Percentage of short passes under pressure, progressive passes completed and switches to wide zones to confirm value in build‑up rather than simply “not making errors.”[^5][^1][^2]
- Sweeper actions per 90 (defensive actions outside the box), average defensive line height for the team, and long‑ball recovery rate to quantify his contribution to depth control behind an aggressive press.[^8][^7][^9][^5]

***

## Central centre‑back (libero profile)

The central CB (e.g. Tapsoba) often behaves like a modern libero, anchoring rest‑defence in a 3‑2 structure while also stepping in to break lines with carries and vertical passes when space opens in front. In settled possession he provides central stability underneath the box midfield, ensuring constant access to the ball‑far wing‑back or the far‑side 10 via diagonal switches and controlling the height of the back line in relation to the pressing line.[^1][^2][^3][^5]

Key metrics to monitor:

- Progressive passes and carries per 90, plus completed line‑breaking passes into midfield and half‑spaces, to verify that he’s an active “connector,” not a static recycler.[^3][^5][^1]
- Duel win rate and interceptions in central zones, plus shots conceded per opposition possession, to assess rest‑defence solidity when the team counter‑presses and leaves him exposed.[^2][^5][^3]
- Pass network centrality (degree/flow centrality) to ensure he is a main node in circulation in Alonso’s structured build‑up.[^5]

***

## Wide centre‑backs

The wide CBs operate as hybrid defenders, responsible for wide channel coverage in defensive transitions and wide build‑up conduits in possession, often stepping into the half‑space to create a temporary back‑two plus advanced wing‑back. In pressing they must be comfortable jumping out of the line to follow dropping forwards or half‑space 10s into midfield, trusting the rest‑defence to rebalance behind them, while on the ball they frequently play penetrative diagonals into advanced wing‑backs or interior 10s.[^1][^2][^3][^5]

Key metrics to monitor:

- Defensive duels and tackles in wide defensive third, plus successful pressures when isolated 1v1 against wingers after rest‑defence shifts, as a proxy for how well they protect aggressive wing‑backs.[^2][^3][^5]
- Progressive passes from wide build‑up zones and diagonal entries into final third to measure their ability to bypass pressure and find high wing‑backs early.[^3][^5][^1]
- Turnovers under pressure in own half and xG conceded directly following those turnovers to understand risk‑management when they step in with the ball.[^7][^5]

***

## Primary 6 in the double pivot (Xhaka profile)

The primary 6 (e.g. Xhaka) is the tactical metronome and positional reference of the whole structure, sitting at the base of the box in possession and providing constant diagonals to both wide CBs and both 10s. He must be able to receive under pressure in central corridors, play first‑time to bounce the press, switch play to the far wing‑back, and occasionally step into the final third to support combinations around the box while still protecting rest‑defence.[^6][^5][^1][^2][^3]

Key metrics to monitor:

- Passes received and completed under pressure in central zones, progressive passes, and switches of play per 90, to confirm his capacity to dominate tempo and break lines from deep.[^5][^1][^3]
- Ball losses in own half and central turnover‑to‑shot‑against rate, as central turnovers are fatal in a box‑midfield system that commits many numbers ahead of the ball.[^7][^5]
- Pressures and recoveries in the middle third immediately after loss (counter‑press events), as Alonso’s model relies on the pivot to “anchor” counter‑pressing in the central lane.[^4][^6][^8][^5]

***

## Secondary 6/8 in the double pivot

The second midfielder (e.g. Palacios) shuttles between being a second 6 in build‑up and an 8 arriving higher between lines, often covering the ball‑side half‑space when the 10 vacates to drag defenders or when the wing‑back makes an underlap. Out of possession, he is the primary connector between the front line and the back three in the mid‑block, responsible for closing interior lanes, screening the opposition 10 and stepping out to press the ball‑near pivot as the trigger is met.[^4][^1][^2][^3][^5]

Key metrics to monitor:

- Third‑man involvement: key passes or pre‑assists following his involvement in combination chains, and progressive receptions in the half‑space when he advances from the pivot line.[^1][^3][^5]
- Pressures, interceptions and recoveries in the middle and high thirds, especially within 5 seconds of loss, as this role is central to the success of Alonso’s counter‑press traps.[^10][^8][^4][^5]
- Distance covered at high intensity and repeat high‑intensity efforts, to ensure he can physically sustain the shuttle role between screening and supporting attacks.[^4][^2][^5]

***

## Wing‑backs (asymmetrical: Grimaldo / Frimpong)

Alonso’s wing‑backs are primary attackers rather than auxiliary full‑backs: they provide width, verticality and a huge share of the team’s goal contributions, with players like Grimaldo and Frimpong combining for very high combined goals+assists from wing‑back. The structure is asymmetrical: at times one wing‑back joins the forward line as an almost second striker, while the far‑side wing‑back holds a slightly deeper and narrower lane to stabilise rest‑defence, which creates an in‑possession 3‑2‑5 with one very high and one more balanced wide player.[^11][^2][^3][^4][^5][^1]

Key metrics to monitor:

- Non‑penalty xG and xA per 90, plus shots and key passes from wide and half‑space zones, since Alonso’s system is explicitly designed to leverage wing‑backs as major end‑product sources.[^2][^3][^1]
- Carries and progressive runs into the final third and penalty area, plus successful 1v1s and cutbacks, to profile their ability to exploit the space created by central overloads.[^3][^4][^5][^2]
- Defensive contribution: pressures and recoveries in wide defensive third and track‑back sprints, measuring how well they rejoin the back line when the team drops into a 5‑2‑2‑1 or 4‑2‑3‑1 defensive shape.[^5][^2]

***

## Attacking midfielders / half‑space 10s

The two 10s (e.g. Wirtz and Hofmann) operate in the half‑spaces, constantly rotating with the wing‑backs and the 9 to create overloads and third‑man options while largely avoiding fixed occupation of the wide channel. They must receive between lines on the half‑turn, threaten depth with runs beyond the 9, and be comfortable dropping onto the pivot line to help progress if the opposition locks the centre, effectively flexing between 10, 8 and even false‑winger roles.[^12][^4][^1][^2][^3][^5]

Key metrics to monitor:

- Half‑space receptions between the lines and progressive receptions in the central corridor, along with xA, key passes and through‑balls, to evaluate their impact as playmakers in Alonso’s central‑dominant model.[^4][^1][^3][^5]
- Non‑penalty xG, shots from zone 14 and touches in the box, since they are encouraged to arrive as finishers, not just facilitators, especially on late box entries when wing‑backs pin the back line.[^2][^3][^5]
- Pressures and recoveries in the high and middle thirds, particularly following lost balls in the interior, as the 10s are critical to “closing the net” on the ball‑carrier in counter‑pressing traps.[^10][^8][^4][^5]

***

## Centre forward

The 9 (e.g. Boniface) is a reference point who pins the last line centrally but is also asked to participate in short combinations, dropping into the box midfield to create numerical superiority before spinning out to attack depth. In the press he is often the first trigger, initiating a curved press on the ball‑carrying centre‑back to block the return pass while using his cover shadow to screen the 6, with the 10s and near wing‑back jumping to close the rest of the first build‑up line.[^13][^8][^1][^3][^4][^5][^2]

Key metrics to monitor:

- Non‑penalty xG, shots per 90 and touches in the opposition box, but also expected goals chain (xGChain) to capture his role as a wall‑pass option in combination moves even when he doesn’t take the final shot.[^14][^3][^5]
- Lay‑off and one‑touch pass completion under pressure, progressive passes received, and on‑ball losses in central zones, to understand how well he can function as a “backboard” in crowded central spaces.[^1][^3][^4][^5]
- Pressures in the final third, high turnovers forced and xG from shots taken within 10 seconds of his team regaining the ball high, which quantify his contribution to Alonso’s aggressive, chance‑creating press.[^14][^8][^10][^7][^5]

***

## Front unit as pressing block

Beyond individual roles, the front three (9 + two 10s or a 9 + two wide forwards at Madrid) act as a synchronised pressing block, with specific triggers for when the ball is played back to the goalkeeper or towards a “locked” flank that activate jump‑presses from the near wing‑back and stepping out from the wide CB. Alonso’s teams use a structured high press quantified by relatively low PPDA values and a high volume of defensive actions (pressures, tackles, interceptions) in the attacking 60% of the pitch, illustrating how much of their chance creation flows directly from ball‑regains rather than from deep construction alone.[^13][^8][^10][^7][^4][^5][^2]

Key metrics to monitor:

- Team‑level PPDA (passes allowed per defensive action) in the high and middle thirds as a primary indicator of pressing intensity and style.[^9][^8][^10][^7]
- High regains (possessions won within 40m of the opposition goal) and shots/xG within 10 seconds of those regains, capturing how well pressing is being converted into direct attacking output.[^10][^14][^7][^5]
- Opposition pass completion and progression rates out of their own third vs league baseline, to compare how effectively Alonso’s pressing block suppresses build‑up relative to other teams.[^8][^7][^10][^5]

Taken together, this positional framework plus the associated metrics gives you a Pro‑Licence level lens on what Alonso’s system actually demands from each role and how to verify, with data, whether the game model is being executed by the right player profiles.
<span style="display:none">[^15]</span>

<div align="center">⁂</div>

[^1]: https://www.discountfootballkits.com/blog/xabi-alonso-a-tactical-breakdown/

[^2]: https://soccer-coaches.com/tactical-masterclass-xabi-alonsos-bayer-leverkusen/

[^3]: https://www.soccertutor.com/blogs/inside-football-coaching/xabi-alonso-tactics-bayer-leverkusen-3-2-5-attacking-shape-wing-back-threat

[^4]: https://kharasportsdaily.com/xabi-alonso-leverkusen-tactics/

[^5]: https://ac3lab.github.io/blog/2024/post_leverkusen_1_en/

[^6]: https://en.wikipedia.org/wiki/Xabi_Alonso

[^7]: https://blogarchive.statsbomb.com/articles/soccer/defensive-metrics-measuring-the-intensity-of-a-high-press/

[^8]: https://theanalyst.com/articles/real-madrid-xabi-alonso-tactics-carreras-mbappe-2025

[^9]: https://www.footballytics.ch/post/analytics-metriken-erklärt-p90-xg-xa-ppda-padj-xgot

[^10]: https://thexgfootballclub.substack.com/p/quantifying-the-intensity-of-high-press-tactics-in-football-with-ppda-37d1ee09f768

[^11]: https://learning.coachesvoice.com/cv/xabi-alonso-tactics-bayer-leverkusen-2022-23/

[^12]: https://themastermindsite.com/2023/09/08/xabi-alonso-bayer-leverkusen-tactical-analysis-2023-24/

[^13]: https://www.youtube.com/watch?v=Y_wxvRpEiNM

[^14]: https://totalfootballanalysis.com/data-analysis/xabi-alonso-real-madrid-tactics-2025-2026-data-analysis

[^15]: https://www.youtube.com/watch?v=WOn5IRd3xQ4

