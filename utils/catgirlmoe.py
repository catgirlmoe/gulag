# -*- coding: utf-8 -*-
import re
from cmyui.discord import Webhook
from cmyui.discord import Embed

from objects import glob
from objects.score import Score
from objects.score import Grade
from objects.player import Player
from objects.beatmap import Beatmap
from objects.match import Match
from objects.match import Slot
from constants.gamemodes import GameMode

CHAT_HOOK = glob.config.webhooks['chat-bridge']
SCORE_HOOK = glob.config.webhooks['score-log']

GRADE_EMOTES = {
  Grade.XH: "<:grade_xh:833673474836660265>",
  Grade.SH: "<:grade_sh:833673474277900318>",
  Grade.X:  "<:grade_x:833673474270167060>",
  Grade.S:  "<:grade_s:833673474022572032>",
  Grade.A:  "<:grade_a:833673433941934091>",
  Grade.B:  "<:grade_b:833673434122289172>",
  Grade.C:  "<:grade_c:833673433656721418>",
  Grade.D:  "<:grade_d:833673433408733194>",
  Grade.F:  "",
  Grade.N:  ""
}

GRADE_COLORS = {
  Grade.XH: 0xE0F7FA, #Silver SS
  Grade.SH: 0xE0F7FA, #Silver S
  Grade.X:  0xFFEB3B, #SS
  Grade.S:  0xFFEB3B, #S
  Grade.A:  0x8BC34A,
  Grade.B:  0x2196F3,
  Grade.C:  0x9C27B0,
  Grade.D:  0xF44336,
  Grade.F:  0x212121,
  Grade.N:  0x212121
}

MOD_EMOTES = {
  'NF': "<:nf:833699841955201114>",
  'EZ': "<:ez:833699842118647819>",
  'TD': "TD",
  'HD': "<:hd:833699841741422642>",
  'HR': "<:hr:833699841644691456>",
  'SD': "<:sd:833699840999424041>",
  'DT': "<:dt:833699841741422645>",
  'RX': "<:rx:833699841267597343>",
  'HT': "<:ht:833699842022178847>",
  'NC': "<:nc:833699841489895488>",
  'FL': "<:fl:833699841510211588>",
  'AU': "<:au:833699842269642762>",
  'SO': "<:so:833699841287782441>",
  'AP': "<:ap:833699842177368125>",
  'PF': "<:pf:833699841510211585>",
  'FI': "FI",
  'RN': "RN",
  'CN': "<:cn:833699841955201115>",
  'TP': "<:tp:833699841288699944>",
  'V2': "V2",
  'MR': "MR",

  '1K': "1K",
  '2K': "2K",
  '3K': "3K",
  '4K': "4K",
  '5K': "5K",
  '6K': "6K",
  '7K': "7K",
  '8K': "8K",
  '9K': "9K",
  'CO': "CO",
}

MODE_EMOTES = {
  GameMode.vn_std: "<:std:835465330204606495>",
  GameMode.vn_taiko: "<:taiko:835465330318508053>",
  GameMode.vn_catch: "<:catch:835465328645242931>",
  GameMode.vn_mania: "<:mania:835465327948333057>",

  GameMode.rx_std: "<:std:835465330204606495> (<:rx:833699841267597343>)",
  GameMode.rx_taiko: "<:taiko:835465330318508053> (<:rx:833699841267597343>)",
  GameMode.rx_catch: "<:catch:835465328645242931> (<:rx:833699841267597343>)",

  GameMode.ap_std: "<:std:835465330204606495> (<:ap:833699842177368125>)",
}

def sanitize(m: str):
  return m.replace("@", "[@]")

async def sendSubmitScore(s: Score):
  wh = Webhook(url=SCORE_HOOK)

  diff=[f'{s.sr:.2f}★']
  if s.mods:
    diff.insert(1, f'({"".join(map(lambda mod: MOD_EMOTES[mod], re.findall("..",repr(s.mods).replace("DTNC","NC"))))})')

  e = Embed(title=s.bmap.full, url=f'https://osu.ppy.sh/b/{s.bmap.id}',color=GRADE_COLORS[s.grade])
  e.set_author(name=f'{s.player.name} achieved #{s.rank} in {MODE_EMOTES[s.mode]}', url=f'https://osu.catgirl.moe/u/{s.player.id}', icon_url=f'https://a.osu.catgirl.moe/{s.player.id}')
  e.add_field("Difficulty:", ' '.join(diff), True)
  e.add_field("Accuracy:", f'{s.acc:.2f}% {GRADE_EMOTES[s.grade]} ({s.pp:,.2f}pp)', True)
  e.add_field("Score:", f'{s.score:,} ({s.max_combo:,}/{s.bmap.max_combo:,}x)', True)
  e.set_image(url=f'https://assets.ppy.sh/beatmaps/{s.bmap.set_id}/covers/cover.jpg')

  wh.add_embed(e)
  await wh.post(glob.http)

async def sendLogin(p: Player):
  wh = Webhook(url=CHAT_HOOK, content=f'📥 **{sanitize(p.name)}** has joined the game.')
  await wh.post(glob.http)

async def sendLogout(p: Player):
  wh = Webhook(url=CHAT_HOOK, content=f'📤 **{sanitize(p.name)}** has left the game.')
  await wh.post(glob.http)

async def sendRankMap(p: Player, b: Beatmap, s: str):
  wh = Webhook(url=CHAT_HOOK)

  e = Embed(title=b.full, url=f'https://osu.ppy.sh/b/{b.id}', color=0xE91E63)
  e.set_author(name=f'{p.name} {s} a map', url=f'https://osu.catgirl.moe/u/{p.id}', icon_url=f'https://a.osu.catgirl.moe/{p.id}')
  e.set_image(url=f'https://assets.ppy.sh/beatmaps/{b.set_id}/covers/cover.jpg')
  
  wh.add_embed(e)
  await wh.post(glob.http)

async def sendSendMessage(p: Player, m: str):
  wh = Webhook(url=CHAT_HOOK, username=p.name, avatar_url=f'https://a.osu.catgirl.moe/{p.id}', content=sanitize(m))
  await wh.post(glob.http)

async def sendMatchCreate(p: Player, m: Match):
  wh = Webhook(url=CHAT_HOOK, content=f'⭐ **{sanitize(p.name)}** created  lobby *"{sanitize(m.name)}"*.')
  await wh.post(glob.http)

async def sendMatchJoin(p: Player, m: Match):
  wh = Webhook(url=CHAT_HOOK, content=f'➡️ **{sanitize(p.name)}** joined lobby *"{sanitize(m.name)}"*.')
  await wh.post(glob.http)

async def sendMatchPart(p: Player, m: Match):
  wh = Webhook(url=CHAT_HOOK, content=f'⬅️ **{sanitize(p.name)}** left lobby *"{sanitize(m.name)}"*.')
  await wh.post(glob.http)

async def sendMatchComplete(slots: list[Slot], m: Match):
  submitted, not_submitted = await m.await_submissions(slots)
  print(submitted)
  print(not_submitted)
  if submitted:
    player_names = []
    player_accuracy = []
    player_scores = []

    wh = Webhook(url=CHAT_HOOK)

    bmap = next(iter(submitted)).recent_score.bmap

    e = Embed(title=bmap.full, url=f'https://osu.ppy.sh/b/{bmap.id}',color=0xF44336)
    for p, z in sorted(submitted.items(), key=lambda item: item[0].recent_score.score, reverse=True):
      s = p.recent_score
      player_names.append(p.name)
      player_accuracy.append(f'{s.acc:.2f}% {GRADE_EMOTES[s.grade]} ({s.pp:,.2f}pp)')
      player_scores.append(f'{s.score:,} ({s.max_combo:,}/{s.bmap.max_combo:,}x)')

    e.set_author(name=f'Lobby "{sanitize(m.name)}" finished a map')
    e.add_field("Players:", '\n'.join(player_names), True)
    e.add_field("Accuracy:", '\n'.join(player_accuracy), True)
    e.add_field("Score:", '\n'.join(player_scores), True)
    e.set_image(url=f'https://assets.ppy.sh/beatmaps/{bmap.set_id}/covers/cover.jpg')
    wh.add_embed(e)
    await wh.post(glob.http)