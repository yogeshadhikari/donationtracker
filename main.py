from enum import member
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from discord import Embed, ButtonStyle
import json
import os
import asyncio
import sympy
from dotenv import load_dotenv

load_dotenv()

# ------------------ File Paths ------------------
MEMBER_FILE = "members.json"
DATA_FILE = "donation_data.json"
MEMBER_JSON_PATH = "member.json"
EXP_FILE = "exp_data.json"
PAGE_SIZE = 10


#____________________Load EXP data________________________
class BulkExp(commands.Cog):

    class ExpCommands(commands.Cog):

        def __init__(self, bot):
            self.bot = bot
            self.members_file = "members.json"
            self.exp_file = "exp_data.json"

            # Load or initialize EXP data
            if os.path.exists(self.exp_file):
                with open(self.exp_file, "r") as f:
                    self.exp_data = json.load(f)
            else:
                self.exp_data = {}


class AddExpCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------ Load Member List ------------------
if os.path.exists(MEMBER_JSON_PATH):
    with open(MEMBER_JSON_PATH, "r") as f:
        try:
            data = json.load(f)
            member_list = data.get("members", [])
        except json.JSONDecodeError:
            member_list = []
else:
    member_list = [
        "bruhid548",
        "IHeartCryptic",
        "Poison_RulzZz",
        "BKball_MASTER",
        "Traitors_Requim05",
        "Osbsshadow",
        "Itachi_Uchiha10180",
        "MissRoyal675",
        "Ares8023",
        "Why_border",
        "Adelarosar",
        "Hhhgggfff40",
        "fsighdjsf",
        "Ishikawa0104",
        "Nepal2_AUSboy",
        "xXxdPantherxXx",
        "abobaclat",
        "Steovell",
        "RimuruTempestXI",
        "limzhengkang",
        "BeastPower321",
        "faroutmanksksk",
        "JOshMirj",
        "Unzknxwn",
        "Sasquatch659",
        "electronicboy7383",
        "JEVONGEMING",
        "jonasNAMIKASE",
        "scratchyyt_1",
        "lilah_mala2",
        "PleasantMazy123",
        "DeanoHendo",
        "Gabiomegapro",
        "PRECKERJ",
        "257bruh",
        "BayPG_05",
        "F411_Guys",
        "RRfamily12",
        "Xxxshaterxx",
        "MKEY901",
        "ethantres12345",
        "Belack82",
        "SterbenedDeath",
        "ytfrul",
        "KeY_4271",
        "iamspidey68",
        "gopeytas",
        "John_200918",
        "Jay472677",
        "bombana_028",
        "LOGANISGOATEDATBD",
        "NgocCanhNe01",
        "DOVAHKIIN1292",
        "Ayanshpro13",
        "iamcookegod",
        "tai24112003",
        "Whixz_Y0sh4",
        "Lethalgn2009",
        "Pinkleafisthebest145",
        "Bldeckm",
        "yoyohanih",
    ]
    # Save the default list to member.json
    with open(MEMBER_JSON_PATH, "w") as f:
        json.dump({"members": member_list}, f, indent=2)

# ------------------ Load Donation Data ------------------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        donation_data = json.load(f)
else:
    donation_data = {"previous": {}, "current": {}}
    with open(DATA_FILE, "w") as f:
        json.dump(donation_data, f)

# ------------------ Discord Bot Setup ------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ------------------ Utility Functions ------------------
def convert_to_number(value: str) -> float:
    units = {
        "Sx": 1e21,
        "Qi": 1e18,
        "Qa": 1e15,
        "T": 1e12,
        "B": 1e9,
        "M": 1e6,
        "K": 1e3
    }
    value = value.strip()
    for unit, factor in units.items():
        if value.endswith(unit):
            try:
                return float(value[:-len(unit)]) * factor
            except:
                return 0.0
    try:
        return float(value)
    except:
        return 0.0


def format_donation(amount: float) -> str:
    units = [("Sx", 1e21), ("Qi", 1e18), ("Qa", 1e15), ("T", 1e12), ("B", 1e9),
             ("M", 1e6), ("K", 1e3)]
    for unit, factor in units:
        if abs(amount) >= factor:
            return f"{round(amount / factor, 2)}{unit}"
    return str(round(amount, 2))


def load_members():
    if os.path.exists(MEMBER_FILE):
        with open(MEMBER_FILE, "r") as f:
            return json.load(f)
    return []


member_list = load_members()


def save_members():
    with open(MEMBER_FILE, "w") as f:
        json.dump(member_list, f)


def save_donations():
    with open(DATA_FILE, "w") as f:
        json.dump(donation_data, f, indent=2)


def format_table(rows: list[str], headers=("Name", "Donation")) -> str:
    max_name = max(len(r.split('|')[0].strip()) for r in rows) if rows else 10
    max_donation = max(len(r.split('|')[1].strip())
                       for r in rows) if rows else 10
    header_line = f"{headers[0]:<{max_name}} | {headers[1]:<{max_donation}}"
    separator = "-" * (max_name + max_donation + 3)
    return f"```{header_line}\n{separator}\n" + "\n".join(rows) + "```"


def update_previous_before_single(name: str):
    current = donation_data.get("current", {})
    previous = donation_data.get("previous", {})

    # Move current donation to previous for this user
    if name in current:
        previous[name] = current[name]
        donation_data["previous"] = previous

        # ------------------ For EXP -----------------


# ------------------ Events ------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} commands.")
    except Exception as e:
        print(f"❌ Sync failed: {e}")


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await asyncio.sleep(2)  # small delay to avoid triggering API too fast


# ------------------ Commands ------------------


@bot.tree.command(name="donations",
                  description="Input all donations at once (comma-separated)")
@app_commands.describe(
    all_donations="Enter donation values in order (e.g., 1T, 2.5Qi, 3.2Sx)")
@commands.cooldown(1, 5, commands.BucketType.user)
async def donations(interaction: discord.Interaction, all_donations: str):
    values = [v.strip() for v in all_donations.split(",")]
    if len(values) != len(member_list):
        await interaction.response.send_message(
            f"❌ Expected {len(member_list)} values, got {len(values)}.")
        return

    donation_data["previous"] = donation_data.get("current", {}).copy()
    donation_data["current"] = {
        name: val
        for name, val in zip(member_list, values)
    }
    save_donations()

    await interaction.response.send_message(
        "✅ All donations updated successfully.")


# ------------------ Single Donation ------------------


@bot.tree.command(name="donate_single",
                  description="Update donation for a single member")
@app_commands.describe(name="Member name",
                       donation="Donation value (e.g., 500Qi)")
async def donate_single(interaction: discord.Interaction, name: str,
                        donation: str):
    if name not in member_list:
        await interaction.response.send_message("❌ Member not found.",
                                                ephemeral=True)
        return

    update_previous_before_single(name)
    donation_data["current"][name] = donation
    save_donations()
    await interaction.response.send_message(
        f"✅ Updated donation for **{name}** to **{donation}**.")


# Autocomplete for the name field
@donate_single.autocomplete("name")
async def name_autocomplete(interaction: discord.Interaction, current: str):
    suggestions = [
        app_commands.Choice(name=m, value=m) for m in member_list
        if current.lower() in m.lower()
    ][:25]  # Discord allows a max of 25 suggestions
    return suggestions


# ------------------ Show All Donations ------------------


@bot.tree.command(name="show_donations",
                  description="Show current donation values")
async def show_donations(interaction: discord.Interaction):
    current = donation_data.get("current", {})
    rows = [f"{name:<20} | {current.get(name, 'N/A')}" for name in member_list]
    await interaction.response.send_message("💎 **Current Donations:**\n" +
                                            format_table(rows))


# ------------------ Weekly Summary ------------------


@bot.tree.command(name="weekly_summary",
                  description="Show donation differences from last week")
@app_commands.describe(
    only_positive="Show only members who increased their donations")
async def weekly_summary(interaction: discord.Interaction,
                         only_positive: bool = False):
    current = donation_data.get("current", {})
    previous = donation_data.get("previous", {})
    summary_rows = []
    for name in member_list:
        curr = convert_to_number(current.get(name, "0"))
        prev = convert_to_number(previous.get(name, "0"))
        diff = curr - prev
        if only_positive and diff <= 0:
            continue
        summary_rows.append((name, prev, curr, diff))
    summary_rows.sort(key=lambda x: x[3], reverse=True)
    if not summary_rows:
        await interaction.response.send_message(
            "No members found with positive donation difference.")
        return

    def get_rank_emoji(index):
        return ["🥇", "🥈", "🥉"][index] if index < 3 else ""

    def build_page(rows, start_index):
        description = "```plaintext\n"
        description += f"{'Member':<20} | {'Previous':<10} | {'Current':<10} | {'Diff'}\n"
        description += f"{'-'*15}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}\n"
        for name, prev, curr, diff in rows:
            description += f"{name:<20} | {format_donation(prev):<10} | {format_donation(curr):<10} | {format_donation(diff)}\n"
        description += "```"
        return "📊 **Weekly Donation Summary**\n" + description

    pages = []
    chunk_size = 30  # Number of entries per page
    for i in range(0, len(summary_rows), chunk_size):
        chunk = summary_rows[i:i + chunk_size]
        page_text = build_page(chunk, i)
        if i + chunk_size >= len(summary_rows):
            total_gain = sum(diff for _, _, _, diff in summary_rows)
            page_text += f"\n**Total Weekly Gain: {format_donation(total_gain)}**"
        pages.append(page_text)
    await interaction.response.send_message(pages[0])
    message = await interaction.original_response()
    if len(pages) > 1:
        await message.add_reaction("⏮")
        await message.add_reaction("⏭")

        def check(reaction, user):
            return (user == interaction.user
                    and str(reaction.emoji) in ["⏮", "⏭"]
                    and reaction.message.id == message.id)

        page_index = 0
        while True:
            try:
                reaction, _ = await bot.wait_for("reaction_add",
                                                 timeout=900.0,
                                                 check=check)
                if str(reaction.emoji) == "⏭":
                    page_index = (page_index + 1) % len(pages)
                elif str(reaction.emoji) == "⏮":
                    page_index = (page_index - 1) % len(pages)
                await message.edit(content=pages[page_index])
                await message.remove_reaction(reaction, interaction.user)
            except asyncio.TimeoutError:
                break


# ------------------ Top Donor ------------------


@bot.tree.command(name="top_donors", description="Show top 3 donors")
async def top_donors(interaction: discord.Interaction):
    current = donation_data.get("current", {})
    sorted_donors = sorted(current.items(),
                           key=lambda x: convert_to_number(x[1]),
                           reverse=True)
    medals = ["🥇", "🥈", "🥉"]
    result = "\n".join(f"{medals[i]} {name}: {amount}"
                       for i, (name, amount) in enumerate(sorted_donors[:3]))
    await interaction.response.send_message(f"🏆 **Top 3 Donors:**\n{result}")


# ------------------ See Donation of Particular Member ------------------


@bot.tree.command(name="donation_of",
                  description="Display the donation of a specific member")
@app_commands.describe(name="Member name")
async def donation_of(interaction: discord.Interaction, name: str):
    if name not in member_list:
        await interaction.response.send_message("❌ Member not found.",
                                                ephemeral=True)
        return

    current = donation_data.get("current", {}).get(name, "0")
    previous = donation_data.get("previous", {}).get(name, "0")
    current_val = convert_to_number(current)
    previous_val = convert_to_number(previous)
    diff = current_val - previous_val

    embed = discord.Embed(title=f"Donation Report: {name}", color=0x00ff99)
    embed.add_field(name="Previous",
                    value=format_donation(previous_val),
                    inline=True)
    embed.add_field(name="Current",
                    value=format_donation(current_val),
                    inline=True)
    embed.add_field(name="Change",
                    value=f"+{format_donation(diff)}"
                    if diff >= 0 else format_donation(diff),
                    inline=True)

    await interaction.response.send_message(embed=embed)


@donation_of.autocomplete("name")
async def donation_of_autocomplete(interaction: discord.Interaction,
                                   current: str):
    return [
        app_commands.Choice(name=m, value=m) for m in member_list
        if current.lower() in m.lower()
    ][:25]


# ------------------ List To Show Who didn't complete weekly ------------------


@bot.tree.command(name="low_donors",
                  description="List members below 6Sx this week")  #6Sx
async def low_donors(interaction: discord.Interaction):
    current = donation_data.get("current", {})
    previous = donation_data.get("previous", {})
    low = []

    for name in member_list:
        curr = convert_to_number(current.get(name, "0"))
        prev = convert_to_number(previous.get(name, "0"))
        diff = curr - prev
        if diff < 6e21:  # 500Qi 6e21
            low.append(f"{name:<21} | {format_donation(diff)}")

    if not low:
        await interaction.response.send_message(
            "✅ Everyone donated at least 6Sx!")
    else:
        await interaction.response.send_message(
            "⚠️ **Members below 6Sx:**\n" +
            format_table(low, headers=("Name", "This Week")))


# ------------------ Add New Hired Member to tracking System ------------------


@bot.tree.command(name="add_member",
                  description="Add a member to tracking list")
@app_commands.describe(name="Exact display name to track")
async def add_member(interaction: discord.Interaction, name: str):
    global member_list  # Ensure we're updating the global list

    # Load existing members from file
    if os.path.exists(MEMBER_JSON_PATH):
        with open(MEMBER_JSON_PATH, "r") as f:
            try:
                data = json.load(f)
                member_list = data.get("members", [])
            except json.JSONDecodeError:
                member_list = []
    else:
        member_list = []

    # Check for duplicate
    if name in member_list:
        await interaction.response.send_message("⚠️ Member already exists.",
                                                ephemeral=True)
        return

    # Add member
    member_list.append(name)

    # Save to file
    with open(MEMBER_JSON_PATH, "w") as f:
        json.dump({"members": member_list}, f, indent=4)

    await interaction.response.send_message(f"✅ Added member: `{name}`")


# ------------------ Remove Member If they Are kicked out of the Guild ------------------


@bot.tree.command(name="remove_member",
                  description="Remove a member from tracking")
@app_commands.describe(name="Exact name to remove")
async def remove_member(interaction: discord.Interaction, name: str):
    # Load members
    with open("members.json", "r") as f:
        member_list = json.load(f)

    if name not in member_list:
        await interaction.response.send_message("❌ Member not found.",
                                                ephemeral=True)
        return

    # Remove from member list
    member_list.remove(name)
    with open("members.json", "w") as f:
        json.dump(member_list, f, indent=4)

    # Remove from donation_data
    if os.path.exists("donation_data.json"):
        with open("donation_data.json", "r") as f:
            donation_data = json.load(f)
        donation_data["current"].pop(name, None)
        donation_data["previous"].pop(name, None)
        with open("donation_data.json", "w") as f:
            json.dump(donation_data, f, indent=4)

    # Remove from exp_data
    if os.path.exists("exp_data.json"):
        with open("exp_data.json", "r") as f:
            exp_data = json.load(f)
        exp_data["current"].pop(name, None)
        exp_data["previous"].pop(name, None)
        with open("exp_data.json", "w") as f:
            json.dump(exp_data, f, indent=4)

    await interaction.response.send_message(
        f"🗑️ Permanently removed member: `{name}`")


# ------------------ List Of All Currnent Guild Members ------------------


@bot.tree.command(name="list_members", description="List all tracked members")
async def list_members(interaction: discord.Interaction):
    members = "\n".join(member_list)
    await interaction.response.send_message(
        f"🧑‍🤝‍🧑 Currnent Guild Members:\n{members}")


# ------------------ Reset All Donations ------------------


@bot.tree.command(name="donation_reset",
                  description="Reset all current donations to zero")
async def donation_reset(interaction: discord.Interaction):
    donation_data["current"] = {
        name: "0"
        for name in member_list
    }  # Reset donations to 0
    save_donations()
    await interaction.response.send_message(
        "✅ All donations have been reset to zero.")


# ------------------ For EXP FUNCTIONS ------------------
@bot.tree.command(name="add_exp", description="Add EXP for a single member")
@app_commands.describe(member_name="Name of the member", exp="New EXP value")
async def add_exp(interaction: discord.Interaction, member_name: str,
                  exp: int):
    with open("members.json", "r") as f:
        member_list = json.load(f)

    if member_name not in member_list:
        await interaction.response.send_message(
            f"❌ Member `{member_name}` not found in members.json.",
            ephemeral=True)
        return

    with open("exp_data.json", "r") as f:
        exp_data = json.load(f)

    # Update previous with current value
    previous_value = exp_data["current"].get(member_name, 0)
    exp_data["previous"][member_name] = previous_value

    # Set new current value
    exp_data["current"][member_name] = exp

    with open("exp_data.json", "w") as f:
        json.dump(exp_data, f, indent=4)

    await interaction.response.send_message(
        f"✅ EXP for `{member_name}` updated.\nPrevious: `{previous_value}`\nCurrent: `{exp}`"
    )


@bot.tree.command(name="bulk_exp",
                  description="Add EXP for all members at once")
@app_commands.describe(
    exp_values="EXP values separated by spaces, in order of members.json")
@commands.cooldown(1, 5, commands.BucketType.user)
async def bulk_exp(interaction: discord.Interaction, exp_values: str):
    await interaction.response.defer(thinking=True)

    with open("members.json", "r") as f:
        member_list = json.load(f)

    exp_input = exp_values.split()

    if len(exp_input) != len(member_list):
        await interaction.followup.send(
            f"❌ You provided {len(exp_input)} EXP values but there are {len(member_list)} members.",
            ephemeral=True)
        return

    with open("exp_data.json", "r") as f:
        exp_data = json.load(f)

    response_lines = []
    for i, member in enumerate(member_list):
        new_exp = int(exp_input[i])
        prev_exp = exp_data["current"].get(member, 0)
        exp_data["previous"][member] = prev_exp
        exp_data["current"][member] = new_exp
        response_lines.append(f"`{member}` ➤ {prev_exp} → {new_exp}")

    with open("exp_data.json", "w") as f:
        json.dump(exp_data, f, indent=4)

    # Paginate result (25 per page)
    pages = []
    for i in range(0, len(response_lines), 25):
        chunk = response_lines[i:i + 25]
        page = "✅ **Bulk EXP Updated**\n" + "\n".join(chunk)
        pages.append(page)

    # Simple pagination buttons
    current_page = 0

    async def update_page(message, page_index):
        await message.edit(content=pages[page_index],
                           view=PaginationView(page_index, len(pages),
                                               update_page))

    class PaginationView(discord.ui.View):

        def __init__(self, page_index, total_pages, callback):
            super().__init__(timeout=60)
            self.page_index = page_index
            self.total_pages = total_pages
            self.callback = callback

        @discord.ui.button(label="Previous",
                           style=discord.ButtonStyle.secondary)
        async def previous(self, interaction_button: discord.Interaction, _):
            if self.page_index > 0:
                self.page_index -= 1
                await self.callback(interaction_button.message,
                                    self.page_index)
                await interaction_button.response.defer()

        @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
        async def next(self, interaction_button: discord.Interaction, _):
            if self.page_index < self.total_pages - 1:
                self.page_index += 1
                await self.callback(interaction_button.message,
                                    self.page_index)
                await interaction_button.response.defer()

    await interaction.followup.send(content=pages[0],
                                    view=PaginationView(
                                        current_page, len(pages), update_page))


@bot.tree.command(
    name="summary",
    description=
    "Show EXP summary: previous, current, and difference for each member.")
async def summary(interaction: discord.Interaction):
    with open('exp_data.json', 'r') as f:
        data = json.load(f)

    members = data.get("members", [])
    current = data.get("current", {})
    previous = data.get("previous", {})

    if not members:
        await interaction.response.send_message(
            "No members are currently being tracked.", ephemeral=True)
        return

    # Build table rows
    rows = []
    for name in members:
        prev_exp = previous.get(name, 0)
        curr_exp = current.get(name, 0)
        diff = int(curr_exp) - int(prev_exp)
        rows.append((name, prev_exp, curr_exp, diff))

    # Sort by EXP diff (descending)
    rows.sort(key=lambda x: x[3], reverse=True)

    # Pagination
    entries_per_page = 25
    pages = [
        rows[i:i + entries_per_page]
        for i in range(0, len(rows), entries_per_page)
    ]

    embeds = []
    total_exp_gained = sum([row[3] for row in rows])  # Total difference

    for i, page in enumerate(pages):
        description = "```plaintext\n"
        description += f"{'Member':<20} | {'Prev EXP':<10} | {'Curr EXP':<10} | {'Diff'}\n"
        description += f"{'-'*15}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}\n"
        for name, prev, curr, diff in page:
            description += f"{name:<20} | {prev:<10} | {curr:<10} | {diff}\n"

        if i == len(pages) - 1:  # Add total to the last page
            description += f"{'-'*52}\n"
            description += f"{'Total EXP Gained:':<43} {total_exp_gained}\n"
        description += "```"

        embed = discord.Embed(title=f"EXP Summary (Page {i+1}/{len(pages)})",
                              description=description,
                              color=discord.Color.green())
        embeds.append(embed)

        embed = discord.Embed(title=f"EXP Summary (Page {i+1}/{len(pages)})",
                              description=description,
                              color=discord.Color.green())
        embeds.append(embed)

    # Send the first page
    current_page = 0
    message = await interaction.response.send_message(
        embed=embeds[current_page], ephemeral=False)

    # If more than 1 page, add navigation
    if len(embeds) > 1:
        message = await interaction.original_response()
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return (user == interaction.user
                    and str(reaction.emoji) in ["⬅️", "➡️"]
                    and reaction.message.id == message.id)

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add",
                                                    timeout=10000.0,
                                                    check=check)
                if str(reaction.emoji
                       ) == "➡️" and current_page < len(embeds) - 1:
                    current_page += 1
                    await message.edit(embed=embeds[current_page])
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "⬅️" and current_page > 0:
                    current_page -= 1
                    await message.edit(embed=embeds[current_page])
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                break


@bot.tree.command(name="reset_exp",
                  description="Reset all EXP data for all members.")
async def reset_exp(interaction: discord.Interaction):
    try:
        with open("exp_data.json", "r") as f:
            data = json.load(f)

        members = data.get("members", [])
        data["current"] = {member: 0 for member in members}
        data["previous"] = {member: 0 for member in members}

        with open("exp_data.json", "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message(
            "✅ All EXP data has been reset.", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"❌ Failed to reset EXP: {e}",
                                                ephemeral=True)


@bot.tree.command(name="full_summary",
                  description="Show full summary of EXP and Donations")
async def full_summary(interaction: discord.Interaction):
    await interaction.response.defer()

    # Load data
    with open("exp_data.json", "r") as f:
        exp_data = json.load(f)

    with open("donation_data.json", "r") as f:
        donation_data = json.load(f)

    members = exp_data["members"]
    exp_current = exp_data["current"]
    exp_previous = exp_data["previous"]

    donation_current = donation_data["current"]
    donation_previous = donation_data["previous"]

    # Prepare EXP summary pages
    exp_pages = []
    for i in range(0, len(members), 25):
        chunk = members[i:i + 25]
        exp_table = "📊 **EXP SUMMARY**\n```ansi\nName               Current       Previous      Difference\n"
        for name in chunk:
            curr = int(exp_current.get(name, 0))
            prev = int(exp_previous.get(name, 0))
            diff = curr - prev
            exp_table += f"{name:<18} {curr:<13} {prev:<13} {diff:<10}\n"
        exp_table += "```"
        exp_pages.append(exp_table)

    # Prepare Donation summary pages
    donation_pages = []
    for i in range(0, len(members), 25):
        chunk = members[i:i + 25]
        donation_table = "💎 **DONATION SUMMARY**\n```ansi\nName               Current       Previous      Difference\n"
        for name in chunk:
            curr = donation_current.get(name, "0")
            prev = donation_previous.get(name, "0")
            diff = donation_diff(curr, prev)
            donation_table += f"{name:<18} {curr:<13} {prev:<13} {diff:<10}\n"
        donation_table += "```"
        donation_pages.append(donation_table)

    # Combine pages
    all_pages = exp_pages + ["\n\n\n"] + donation_pages

    # Paginate
    current_page = 0

    async def update_page(message, page_index):
        await message.edit(content=all_pages[page_index],
                           view=PaginationView(page_index, len(all_pages),
                                               update_page))

    class PaginationView(discord.ui.View):

        def __init__(self, page_index, total_pages, callback):
            super().__init__(timeout=60)
            self.page_index = page_index
            self.total_pages = total_pages
            self.callback = callback

        @discord.ui.button(label="Previous",
                           style=discord.ButtonStyle.secondary)
        async def previous(self, interaction_button: discord.Interaction, _):
            if self.page_index > 0:
                self.page_index -= 1
                await self.callback(interaction_button.message,
                                    self.page_index)
                await interaction_button.response.defer()

        @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
        async def next(self, interaction_button: discord.Interaction, _):
            if self.page_index < self.total_pages - 1:
                self.page_index += 1
                await self.callback(interaction_button.message,
                                    self.page_index)
                await interaction_button.response.defer()

    await interaction.followup.send(content=all_pages[current_page],
                                    view=PaginationView(
                                        current_page, len(all_pages),
                                        update_page))


def donation_diff(curr: str, prev: str) -> str:
    try:
        from sympy import sympify
        return str(sympify(curr) - sympify(prev))
    except Exception:
        return "?"


#------------------ Start the Bot ------------------#
token = os.getenv("DISCORD_TOKEN")
if token is None:
    print("Error: DISCORD_TOKEN is not set in the environment variables.")
else:
    bot.run(token)
