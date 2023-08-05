# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import ast

from .. import udB


def get_flood():
    n = []
    n.append(ast.literal_eval(udB.get("ANTIFLOOD")))
    return n[0]


def set_flood(chat_id, limit):
    omk = get_flood()
    omk.update({str(chat_id): str(limit)})
    udB.set("ANTIFLOOD", str(omk))
    return True


def get_flood_limit(chat_id):
    omk = get_flood()
    if str(chat_id) in omk.keys():
        return omk[str(chat_id)]
    else:
        return False
