import BasketballRefScraper as brs

TEST_STRING = """
'\n   <div class="table_outer_container">\n      <div class="overthrow table_container" id="div_four_factors">\n  <table
 class="suppress_all sortable stats_table" id="four_factors" data-cols-to-freeze=1><caption>Four Factors Table</caption>
 \n      \n      <tr class="over_header thead">\n         <th aria-label="" data-stat="" colspan="2" class=" over_header
  center" ></th>\n         <th aria-label="" data-stat="header_tmp" colspan="4" class=" over_header center" >Four Factor
  s</th><th></th>\n      </tr>\n      \n\n      \n      <tr class="thead">\n         <th aria-label="Team" data-stat="te
  am_id" class=" sort_default_asc left" data-tip="Team" >&nbsp;</th>\n         <th aria-label="Pace Factor" data-stat="p
  ace" class=" right" data-tip="<b>Pace Factor</b>: An estimate of possessions per 48 minutes" >Pace</th>\n         <th 
  aria-label="Effective Field Goal Percentage" data-stat="efg_pct" class=" center" data-tip="<strong>Effective Field Goa
  l Percentage</strong><br>This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 
  2-point field goal." data-over-header="Four Factors" >eFG%</th>\n         <th aria-label="Turnover Percentage" data-st
  at="tov_pct" class=" sort_default_asc center" data-tip="<b>Turnover Percentage</b><br>An estimate of turnovers commit
  ted per 100 plays." data-over-header="Four Factors" >TOV%</th>\n         <th aria-label="Offensive Rebound Percentage"
  data-stat="orb_pct" class=" center" data-tip="<b>Offensive Rebound Percentage</b><br>An estimate of the percentage of
  available offensive rebounds a player grabbed while he was on the floor." data-over-header="Four Factors" >ORB%</th>
    \n         <th aria-label="Free Throws Per Field Goal Attempt" data-stat="ft_rate" class=" right" data-tip="Free Thr
    ows Per Field Goal Attempt" data-over-header="Four Factors" >FT/FGA</th>\n         <th aria-label="Offensive Rating"
     data-stat="off_rtg" class=" center" data-tip="<b>Offensive Rating</b><br>An estimate of points produced (players) o
     r scored (teams) per 100 possessions" >ORtg</th>\n      </tr>\n      \n\n<tr ><th scope="row" class="left " data-st
     at="team_id" ><a href="/teams/MIN/2020.html">MIN</a></th><td class="right " data-stat="pace" >105.5</td><td class="
     right plus" data-stat="efg_pct" >.539</td><td class="right plus" data-stat="tov_pct" >10.9</td><td class="right pl
     us" data-stat="orb_pct" >29.8</td><td class="right plus" data-stat="ft_rate" >.311</td><td class="right " data-stat
     ="off_rtg" >118.5</td></tr>\n<tr ><th scope="row" class="left " data-stat="team_id" ><a href="/teams/ATL/2020.html"
     >ATL</a></th><td class="right " data-stat="pace" >105.5</td><td class="right minus" data-stat="efg_pct" >.489</td><
     td class="right minus" data-stat="tov_pct" >13.9</td><td class="right minus" data-stat="orb_pct" >21.4</td><td clas
     s="right minus" data-stat="ft_rate" >.223</td><td class="right " data-stat="off_rtg" >107.1</td></tr>\n\n</tbody></
     table>\n\n      </div>\n   </div>\n'
"""

def test_build_season_data():
    pass

def test_get_game_data():
    pass

def test_get_all_4factor_stats():
    pass

def test_get_4factor_stat():
    brs.get_4_factor_stat(TEST_STRING)

def test_get_score(web_string: str):
    pass

def test_get_days_data():
    pass