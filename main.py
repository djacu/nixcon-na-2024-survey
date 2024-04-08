from pathlib import Path
import re

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tabulate import tabulate


def main() -> None:
    data = ingest()
    #plot_usenixbefore(data)
    #plot_usenixhome(data)
    #plot_usenixwork(data)

    #plot_nixexp(data)

    #plot_contentlikertscale_001(data)
    #plot_contentlikertscale_002(data)
    #plot_contentlikertscale_003(data)

    #plot_mostvaluablesession(data)

    #plot_generallikertscale_001(data)
    #plot_generallikertscale_002(data)
    #plot_generallikertscale_003(data)
    #plot_generallikertscale_004(data)

    #plot_eventlikemost(data)
    #plot_eventlikeleast()

    #plot_howhear()
    #plot_whyattend()

    
def ingest() -> pd.DataFrame:
    return pd.read_csv(Path("./results-survey248687.csv"))


def plot_usenixbefore(data: pd.DataFrame) -> None:
    ax = sns.histplot(data['usenixbefore'])
    ax.set(xlabel='Have you used Nix Before?')
    fig = ax.get_figure()
    fig.savefig(Path('./usenixbefore.png'))
    fig.clf()


def plot_usenixhome(data: pd.DataFrame) -> None:
    ax = sns.histplot(data['usenixhome'])
    ax.set(xlabel='Do you use Nix at home?')
    fig = ax.get_figure()
    fig.savefig(Path('./usenixhome.png'))
    fig.clf()


def plot_usenixwork(data: pd.DataFrame) -> None:
    ax = sns.histplot(data['usenixwork'])
    ax.set(xlabel='Do you use Nix at work?')
    fig = ax.get_figure()
    fig.savefig(Path('./usenixwork.png'))
    fig.clf()


def plot_nixexp(data: pd.DataFrame) -> None:
    #print(data[['howfamiliarnix', 'howmanyyears']])
    expdata = data[['howfamiliarnix', 'howmanyyears']]
    expdata['count'] = 1
    pivot = pd.pivot_table(expdata, values='count', index='howfamiliarnix', columns='howmanyyears', aggfunc='sum')

    index_order = ['Expert', 'Intermediate', 'Beginner', 'Never Used/Just Started'];
    column_order = ['Never', '< 1 year', '1 - 2 years', '2 - 3 years', '3 - 4 years', '4 - 5 years', '5 - 10 years', '> 10 years']
    pivot = pivot.reindex(index_order, axis=0)
    pivot = pivot.reindex(column_order, axis=1)
    #print(pivot)

    ax = sns.heatmap(pivot, annot=True, cbar_kws={"shrink": 0.5})
    ax.set_aspect('equal','box')
    ax.set(
            xlabel='How many years have you used Nix?',
            ylabel='How familiar are you with Nix?',
            )
    ax.set_yticklabels(['Expert', 'Intermediate', 'Beginner', 'Never Used\nJust Started'])
    ax.set_xticklabels(['Never', '< 1', '1 - 2', '2 - 3', '3 - 4', '4 - 5', '5 - 10', '> 10'])
    #ax.set_xticklabels(ax.get_xticklabels(), ha='right')
    ax.tick_params(axis='x', rotation=45)
    ax.figure.tight_layout()
    fig = ax.get_figure()
    fig.savefig(Path('./nixexp-heatmap.png'))
    fig.clf()


def plot_contentlikertscale_001(data: pd.DataFrame) -> None:
    ax = sns.histplot(data['contentlikertscale[SQ001]'], discrete=True, binrange=(1, 5))
    ax.set(xlabel='In your opinion, did the conference meet its objectives?')
    ax.set(title='On a scale from 1 to 5.')
    fig = ax.get_figure()
    fig.savefig(Path('./contentlikertscale-001.png'))
    fig.clf()


def plot_contentlikertscale_002(data: pd.DataFrame) -> None:
    ax = sns.histplot(data['contentlikertscale[SQ002]'], discrete=True, binrange=(1, 5))
    ax.set(xlabel='How well was the conference structured?')
    ax.set(title='On a scale from 1 to 5.')
    fig = ax.get_figure()
    fig.savefig(Path('./contentlikertscale-002.png'))
    fig.clf()


def plot_contentlikertscale_003(data: pd.DataFrame) -> None:
    ax = sns.histplot(data['contentlikertscale[SQ003]'], discrete=True, binrange=(1, 5))
    ax.set(xlabel='How satisfied are you with the variety of topics presented at the conference?')
    ax.set(title='On a scale from 1 to 5.')
    fig = ax.get_figure()
    fig.savefig(Path('./contentlikertscale-003.png'))
    fig.clf()


def plot_mostvaluablesession(data: pd.DataFrame) -> None:
    #pd.options.display.max_colwidth = 160
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.width', 1000)

    mvs = data['mostvaluablesession'].to_frame().dropna()

    mvs['intro'] = np.where(mvs['mostvaluablesession'].str.contains(r'Quick|quick|Introduction|introduction|into Nix|beginner', na=False), 1, 0)
    mvs['hm'] = np.where(mvs['mostvaluablesession'].str.contains(r'Home|home|Manager|manager', na=False), 1, 0)
    mvs['modules'] = np.where(mvs['mostvaluablesession'].str.contains(r'Dan|dan|Modules|modules', na=False), 1, 0)
    mvs['ci'] = np.where(mvs['mostvaluablesession'].str.contains(r'ci|CI', na=False), 1, 0)

    mvs['xe'] = np.where(mvs['mostvaluablesession'].str.contains(r'Xe|xe|Docker|docker', na=False), 1, 0)
    mvs['systemd'] = np.where(mvs['mostvaluablesession'].str.contains(r'Systemd|systemd', na=False), 1, 0)
    mvs['contracts'] = np.where(mvs['mostvaluablesession'].str.contains(r'contracts', na=False), 1, 0)
    mvs['builders'] = np.where(mvs['mostvaluablesession'].str.contains(r'Substituters|Substitutes|substituters|Susbtituers', na=False), 1, 0)
    mvs['looker'] = np.where(mvs['mostvaluablesession'].str.contains(r'Google|google|Looker|looker', na=False), 1, 0)
    mvs['bazel'] = np.where(mvs['mostvaluablesession'].str.contains(r'Bazel|robots', na=False), 1, 0)

    mvs['union'] = np.where(mvs['mostvaluablesession'].str.contains(r'State|state|Union|union', na=False), 1, 0)
    mvs['lightning'] = np.where(mvs['mostvaluablesession'].str.contains(r'lightning|Lightening', na=False), 1, 0)

    mvs['sum'] = mvs.drop('mostvaluablesession', axis=1).sum(axis=1)

    mvs_sum = mvs.drop('mostvaluablesession', axis=1).drop('sum', axis=1).sum(axis=0) 

    ax = sns.barplot(mvs_sum)
    ax.tick_params(axis='x', rotation=45)
    ax.set_xticklabels([
        'Intro to Nix',
        'Home-Manager',
        'Basic Modules',
        'CI Hands On',
        'Nix/Docker',
        'Systemd in stage 1',
        'Module contracts',
        'Substituters',
        'Looker',
        'Bazel/Nix/Robots',
        'State of the Union',
        'Lightning talks',
        ])
    ax.set_xticklabels(ax.get_xticklabels(), ha='right')

    ax.set(title='Which session did you find most valuable?')
    ax.set(ylabel='Counts')
    ax.figure.tight_layout()
    fig = ax.get_figure()
    fig.savefig(Path('./mostvaluablesession.png'))
    fig.clf()


def plot_generallikertscale_001(data: pd.DataFrame) -> None:
    ax = sns.histplot(data['generallikertscale[SQ001]'], discrete=True, binrange=(1, 5))
    ax.set(xlabel='How would you rate your overall experience at the event?')
    ax.set(title='On a scale from 1 to 5.')
    fig = ax.get_figure()
    fig.savefig(Path('./generallikertscale-001.png'))
    fig.clf()


def plot_generallikertscale_002(data: pd.DataFrame) -> None:
    ax = sns.histplot(data['generallikertscale[SQ002]'], discrete=True, binrange=(1, 5))
    ax.set(xlabel='How satisfied were you with the networking opportunities provided?')
    ax.set(title='On a scale from 1 to 5.')
    fig = ax.get_figure()
    fig.savefig(Path('./generallikertscale-002.png'))
    fig.clf()


def plot_generallikertscale_003(data: pd.DataFrame) -> None:
    ax = sns.histplot(data['generallikertscale[SQ003]'], discrete=True, binrange=(1, 5))
    ax.set(xlabel='How likely are you to recommend this event to a friend?')
    ax.set(title='On a scale from 1 to 5.')
    fig = ax.get_figure()
    fig.savefig(Path('./generallikertscale-003.png'))
    fig.clf()


def plot_generallikertscale_004(data: pd.DataFrame) -> None:
    ax = sns.histplot(data['generallikertscale[SQ004]'], discrete=True, binrange=(1, 5))
    ax.set(xlabel='Were you able to easily find all of the information you need about our event?')
    ax.set(title='On a scale from 1 to 5.')
    fig = ax.get_figure()
    fig.savefig(Path('./generallikertscale-004.png'))
    fig.clf()


def plot_eventlikemost(data: pd.DataFrame) -> None:
    #pd.options.display.max_colwidth = 240
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.width', 1000)
    #print(data['eventlikemost'].dropna().to_string())
    #print(data['eventlikemost'][40])

    #elm = data['eventlikemost'].to_frame().dropna()

    #elm['inperson'] = np.where(elm['eventlikemost'].str.contains(r'Talking|talking|Meeting|meeting|meet|Getting to talk|networking|The people.|in person|connect|chatting|Networking|nice people', na=False), 1, 0)
    #elm['vibes'] = np.where(elm['eventlikemost'].str.contains(r'vibe|Vibe|informal|Informal|nice people|nice everyone', na=False), 1, 0)
    #elm['karaoke'] = np.where(elm['eventlikemost'].str.contains(r'karaoke|Karoke', na=False), 1, 0)
    #elm['sum'] = elm.drop('eventlikemost', axis=1).sum(axis=1)
    ##print(elm);
    #elm_sum = elm.drop('eventlikemost', axis=1).drop('sum', axis=1).sum(axis=0) 

    #ax = sns.barplot(elm_sum)


    grouped_categories = {
        'Meeting People': 12,
        'Talks': 4,
        'Community and Atmosphere': 9,
        'Karaoke': 4,
    }
    ax = sns.barplot(grouped_categories)
    ax.tick_params(axis='x', rotation=45)
    ax.set_xticklabels([
        'Meeting People',
        'Talks',
        'Community\nAtmosphere',
        'Karaoke',
        ])
    ax.set_xticklabels(ax.get_xticklabels(), ha='right')
    ax.yaxis.get_major_locator().set_params(integer=True)

    ax.set(title='What did you like most about the event?')
    ax.set(ylabel='Counts')
    ax.figure.tight_layout()
    fig = ax.get_figure()
    fig.savefig(Path('./eventlikemost.png'))
    fig.clf()


def plot_eventlikeleast() -> None:
    grouped_responses = {
        "Content Quality/Relevance": 8,
        "Logistics/Communication": 4,
        "Technical Issues": 7,
        "Schedule/Duration": 2,
        "Accessibility/Location": 3,
        "Networking Opportunities": 2,
        "Miscellaneous": 6
    }
    ax = sns.barplot(grouped_responses)
    ax.tick_params(axis='x', rotation=45)
    ax.set_xticklabels([
        "Content Quality\nRelevance",
        "Logistics\nCommunication",
        "Technical Issues",
        "Schedule\nDuration",
        "Accessibility\nLocation",
        "Networking\nOpportunities",
        "Miscellaneous"
        ])
    ax.set_xticklabels(ax.get_xticklabels(), ha='right')
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.set(title='What did you like least about the event?')
    ax.set(ylabel='Counts')
    ax.figure.tight_layout()
    fig = ax.get_figure()
    fig.savefig(Path('./eventlikeleast.png'))
    fig.clf()


def plot_howhear() -> None:
    responses = {
        'Referral/Word of Mouth': 18,
        'Podcasts/Shows': 7,
        'Online Communities/Forums': 21,
    }
    ax = sns.barplot(responses)
    ax.tick_params(axis='x', rotation=45)
    ax.set_xticklabels([
        'Referral\nWord of Mouth',
        'Podcasts\nShows',
        'Online Communities\nForums',
        ])
    ax.set_xticklabels(ax.get_xticklabels(), ha='right')
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.set(title='How did you hear about NixCon?')
    ax.set(ylabel='Counts')
    ax.figure.tight_layout()
    fig = ax.get_figure()
    fig.savefig(Path('./howhear.png'))
    fig.clf()


def plot_whyattend() -> None:
    responses = {
        "Interest/Love for Nix": 16,
        "Learning": 19,
        "Networking": 16,
    }
    ax = sns.barplot(responses)
    ax.tick_params(axis='x', rotation=45)
    ax.set_xticklabels([
        "Interest\nLove for Nix",
        "Learning",
        "Networking",
        ])
    ax.set_xticklabels(ax.get_xticklabels(), ha='right')
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.set(title='Why did you attend NixCon?')
    ax.set(ylabel='Counts')
    ax.figure.tight_layout()
    fig = ax.get_figure()
    fig.savefig(Path('./whyattend.png'))
    fig.clf()


if __name__ == "__main__":
    main()
