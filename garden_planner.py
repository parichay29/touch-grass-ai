"""
Touch Grass AI - Garden Planner
Open-source AI garden planning that runs locally.

No API keys. No cloud. No tracking. Just your garden.
"""

import os
import sys
import argparse
import datetime
from typing import Optional, List, Dict

# Ensure UTF-8 output on Windows terminals
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from frost_dates import get_frost_dates, get_zone_info, FrostDates
from plant_database import (
    PLANT_DATABASE, search_plants, get_plant, plants_for_zone,
    plants_for_season, companions_for, nitrogen_fixers, get_plant_count,
    Plant, Season
)
from prompts import (
    GARDEN_ASSISTANT_SYSTEM, FROST_DATE_CONTEXT, PLANT_CONTEXT,
    WEEKLY_CALENDAR_PROMPT, COMPANION_PROMPT, COVER_CROP_PROMPT,
    PERSONALITY
)
from llm_engine import LocalLLM, find_model, list_models

# ANSI colors
class C:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def print_banner():
    """Print the Touch Grass AI banner."""
    banner = f"""{C.GREEN}{C.BOLD}
=======================================================
   *  TOUCH GRASS AI  *

   Open-source garden planner. Runs on your machine.
   No cloud. No API keys. No tracking.
======================================================={C.RESET}
"""
    print(banner)

def print_plant(plant: Plant, indent: str = ""):
    """Pretty print a plant."""
    print(f"{indent}{C.GREEN}{plant.name}{C.RESET} ({plant.type.value}, {plant.days_to_maturity} days)")
    if plant.companions:
        comps = ", ".join([c for c in plant.companions if c])
        if comps:
            print(f"{indent}  🌿 Companions: {comps}")
    if plant.avoid:
        avoid = ", ".join([a for a in plant.avoid if a])
        if avoid:
            print(f"{indent}  🚫 Avoid: {avoid}")
    if plant.pests:
        pests = ", ".join([p for p in plant.pests if p])
        if pests:
            print(f"{indent}  🐛 Pests: {pests}")
    if plant.nitrogen_fixer:
        print(f"{indent}  💚 Nitrogen fixer")
    if plant.perennial:
        print(f"{indent}  ♾️  Perennial")
    if plant.notes:
        print(f"{indent}  📝 {plant.notes}")

def print_weekly_calendar(frost: FrostDates, today: Optional[datetime.date] = None):
    """Calculate and print this week's planting calendar."""
    today = today or datetime.date.today()
    doy = today.timetuple().tm_yday

    print(f"\n{C.CYAN}{C.BOLD}📅 THIS WEEK ({today.strftime('%b %d')}):{C.RESET}")

    # Determine season phase
    last_frost_doy = frost.last_frost_doy
    first_frost_doy = frost.first_frost_doy

    # Classify plants by what to do this week
    to_sow = []
    to_transplant = []
    to_harvest = []
    to_avoid = []

    for plant in PLANT_DATABASE.values():
        # Skip if zone doesn't match
        try:
            zone_num = int(frost.zone[0])
            min_z = int(plant.zone_min[0])
            max_z = int(plant.zone_max[0])
            if not (min_z <= zone_num <= max_z):
                continue
        except (ValueError, IndexError):
            continue

        # Calculate planting windows
        sow_start = last_frost_doy - plant.sow_before_last_frost
        sow_end = last_frost_doy + plant.sow_after_last_frost
        if plant.sow_before_last_frost > 0 and plant.sow_after_last_frost == 0:
            sow_end = sow_start + 14  # ~2 week window

        trans_end = last_frost_doy + plant.transplant_after_last_frost
        if plant.transplant_after_last_frost > 0:
            trans_start = last_frost_doy
            if trans_start <= doy <= trans_end:
                to_transplant.append(plant)

        # Harvest window (approximate)
        harvest_start = sow_start + plant.days_to_maturity
        harvest_end = sow_end + plant.days_to_maturity + 30
        if harvest_start <= doy <= harvest_end:
            to_harvest.append(plant)

        # What to sow now
        if sow_start <= doy <= sow_end:
            to_sow.append(plant)
        elif doy < sow_start - 30 or doy > first_frost_doy:
            # Too early or too late for this plant
            if plant.season == Season.WARM and doy > first_frost_doy - 60:
                to_avoid.append(plant)
            elif plant.season == Season.COOL and doy > first_frost_doy + 30:
                to_avoid.append(plant)

    if to_sow:
        print(f"{C.GREEN}  ✅ SOW:{C.RESET}")
        for p in to_sow[:8]:
            print(f"     • {p.name} ({p.days_to_maturity} days)")

    if to_transplant:
        print(f"{C.CYAN}  🌱 TRANSPLANT:{C.RESET}")
        for p in to_transplant[:8]:
            print(f"     • {p.name}")

    if to_harvest:
        print(f"{C.YELLOW}  🧺 HARVEST:{C.RESET}")
        for p in to_harvest[:8]:
            print(f"     • {p.name}")

    if to_avoid:
        print(f"{C.RED}  🛑 AVOID (too late/early):{C.RESET}")
        for p in to_avoid[:5]:
            print(f"     • {p.name}")

    if not any([to_sow, to_transplant, to_harvest, to_avoid]):
        print("  📭 No specific actions this week. Check back soon!")

def cmd_calendar(args):
    """Print weekly planting calendar."""
    frost = get_frost_dates(args.zip)
    print_banner()
    print(f"{C.GREEN}🌱 Garden Planner for ZIP {frost.zip_code}{C.RESET}")
    print(f"   Zone {frost.zone} ({get_zone_info(frost.zone)['range']})")
    print(f"   Last frost: {frost.last_frost_date.strftime('%B %d')}")
    print(f"   First frost: {frost.first_frost_date.strftime('%B %d')}")
    print(f"   Growing season: {frost.growing_days} days")
    print_weekly_calendar(frost)

def cmd_plant(args):
    """Look up a plant."""
    print_banner()
    query = " ".join(args.name)
    plant = get_plant(query)
    if plant:
        print_plant(plant)
    else:
        results = search_plants(query)
        if results:
            print(f"Found {len(results)} matches:")
            for p in results[:10]:
                print_plant(p, indent="  ")
        else:
            print(f"No plant found for '{query}'")
            print(f"\nTry: python garden_planner.py --list | grep {query}")

def cmd_list(args):
    """List plants by zone or season."""
    print_banner()
    if args.zone:
        plants = plants_for_zone(args.zone)
        print(f"Plants for zone {args.zone} ({len(plants)}):")
        for p in sorted(plants, key=lambda x: x.name):
            print_plant(p, indent="  ")
    elif args.season:
        try:
            season = Season(args.season.lower())
        except ValueError:
            print(f"Invalid season. Use: cool, warm, hot, cold")
            return
        plants = plants_for_season(season)
        print(f"{season.value} season plants ({len(plants)}):")
        for p in sorted(plants, key=lambda x: x.name):
            print_plant(p, indent="  ")
    elif args.nitrogen:
        plants = nitrogen_fixers()
        print(f"Nitrogen-fixing plants ({len(plants)}):")
        for p in sorted(plants, key=lambda x: x.name):
            print_plant(p, indent="  ")
    else:
        print(f"Plant database: {get_plant_count()} plants")
        print("\nCategories:")
        by_type = {}
        for p in PLANT_DATABASE.values():
            by_type.setdefault(p.type.value, []).append(p)
        for t, plants in sorted(by_type.items()):
            print(f"\n  {t.upper()} ({len(plants)}):")
            names = sorted([p.name for p in plants])
            for i in range(0, len(names), 4):
                print(f"    {', '.join(names[i:i+4])}")

def cmd_companions(args):
    """Show companion plants."""
    print_banner()
    result = companions_for(args.name)
    if "error" in result:
        print(result["error"])
        return
    plant = get_plant(args.name)
    print(f"{C.GREEN}Companions for {result['plant']}:{C.RESET}")
    if result["companions"]:
        print(f"  🌿 Good neighbors: {', '.join(result['companions'])}")
    if result["avoid"]:
        print(f"  🚫 Keep away: {', '.join(result['avoid'])}")
    if result["pests"]:
        print(f"  🐛 Watch for: {', '.join(result['pests'])}")
    if plant and plant.notes:
        print(f"  📝 {plant.notes}")

def cmd_ask(args):
    """Ask the AI garden assistant (local model)."""
    frost = get_frost_dates(args.zip)
    print_banner()
    print(f"{C.GREEN}💬 Garden Assistant (local AI){C.RESET}")
    print(f"   Zone {frost.zone} | Last frost: {frost.last_frost_date.strftime('%b %d')} | First frost: {frost.first_frost_date.strftime('%b %d')}")
    print()

    # Build context
    context = FROST_DATE_CONTEXT.format(
        zip_code=frost.zip_code,
        zone=frost.zone,
        last_frost=frost.last_frost_date.strftime('%B %d'),
        first_frost=frost.first_frost_date.strftime('%B %d'),
        growing_days=frost.growing_days,
    )

    # Add plant list
    zone_plants = plants_for_zone(frost.zone)
    plant_names = [p.name for p in zone_plants]
    plant_list = ", ".join(plant_names) if plant_names else "Various seasonal plants"
    context += PLANT_CONTEXT.format(plant_list=plant_list)

    # Find model
    model_path = find_model(args.model)
    if not model_path:
        print("⚠️  No local model found.")
        print("   Run: python download_model.py")
        print("\nFalling back to built-in knowledge base...")
        answer_builtin(args.question, frost)
        return

    print(f"🤖 Loading model: {os.path.basename(model_path)}")
    llm = LocalLLM(model_path, n_ctx=1024, n_threads=os.cpu_count() or 4)

    # Build prompt
    full_prompt = f"""{GARDEN_ASSISTANT_SYSTEM}
{context}
{PERSONALITY}

QUESTION: {args.question}

ANSWER:"""

    print("\n⏳ Thinking...")
    try:
        response = llm.complete(full_prompt, max_tokens=300, temperature=0.7)
        print(f"\n{C.CYAN}🤖 {response}{C.RESET}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Falling back to built-in knowledge...")
        answer_builtin(args.question, frost)

def answer_builtin(question: str, frost: FrostDates):
    """Fallback answer using built-in knowledge (no LLM needed)."""
    q = question.lower()

    # Companion planting queries
    if "companion" in q or "plant together" in q or "next to" in q:
        for name, plant in PLANT_DATABASE.items():
            if name in q:
                result = companions_for(name)
                if "companions" in result:
                    print(f"\n🌿 {result['plant']} companions:")
                    print(f"   Good: {', '.join(result['companions'])}")
                    print(f"   Avoid: {', '.join(result['avoid'])}")
                return

    # Cover crop queries
    if "cover crop" in q or "nitrogen" in q or "green manure" in q:
        print("\n💚 Cover crop recommendations:")
        print(f"   For zone {frost.zone} (last frost {frost.last_frost_date.strftime('%b %d')}):")
        for p in nitrogen_fixers():
            if p.type.value == "cover_crop":
                print(f"   • {p.name}: {p.notes}")
        return

    # Frost queries
    if "frost" in q or "when to plant" in q:
        print(f"\n🌡️  Frost dates for ZIP {frost.zip_code}:")
        print(f"   Last frost: {frost.last_frost_date.strftime('%B %d')}")
        print(f"   First frost: {frost.first_frost_date.strftime('%B %d')}")
        print(f"   Growing days: {frost.growing_days}")
        print(f"   Zone: {frost.zone} ({get_zone_info(frost.zone)['range']})")
        return

    # Pest queries
    if "pest" in q or "bugs" in q or "aphid" in q:
        print("\n🐛 Common organic pest control:")
        print("   • Aphids: spray with water, release ladybugs, plant nasturtiums as trap crop")
        print("   • Cabbage worms: use Bt (Bacillus thuringiensis), row covers")
        print("   • Slugs: beer traps, copper tape, hand-pick at night")
        print("   • Flea beetles: row covers, mulch, neem oil")
        return

    # Default
    print(f"\n🌱 Ask me about:")
    print("   • 'What are good companions for tomatoes?'")
    print("   • 'What cover crop should I plant?'")
    print("   • 'When is the last frost?'")
    print("   • 'How do I deal with aphids?'")
    print("   • 'What can I plant this week?'")

def cmd_chat(args):
    """Interactive chat mode."""
    frost = get_frost_dates(args.zip)
    print_banner()
    print(f"{C.GREEN}💬 Touch Grass AI - Chat Mode{C.RESET}")
    print(f"   Zone {frost.zone} | Last frost: {frost.last_frost_date.strftime('%b %d')}")
    print(f"   Type 'quit' to exit\n")

    model_path = find_model(args.model)
    if not model_path:
        print("⚠️  No local model found. Run: python download_model.py")
        print("   Using built-in knowledge base instead.\n")
        while True:
            try:
                question = input("🌱 You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Happy gardening!")
                break
            if question.lower() in ("quit", "exit", "q"):
                print("👋 Happy gardening!")
                break
            answer_builtin(question, frost)
            print()
        return

    llm = LocalLLM(model_path, n_ctx=1024, n_threads=os.cpu_count() or 4)
    context = FROST_DATE_CONTEXT.format(
        zip_code=frost.zip_code, zone=frost.zone,
        last_frost=frost.last_frost_date.strftime('%B %d'),
        first_frost=frost.first_frost_date.strftime('%B %d'),
        growing_days=frost.growing_days,
    )

    messages = [{"role": "system", "content": GARDEN_ASSISTANT_SYSTEM + "\n" + context}]

    while True:
        try:
            question = input("🌱 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Happy gardening!")
            break
        if question.lower() in ("quit", "exit", "q"):
            print("👋 Happy gardening!")
            break

        messages.append({"role": "user", "content": question})
        print("🤖 Assistant: ", end="", flush=True)
        try:
            response = llm.chat(messages, max_tokens=300, temperature=0.7)
            print(response)
            messages.append({"role": "assistant", "content": response})
        except Exception as e:
            print(f"\n❌ Error: {e}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description="Touch Grass AI - Open-source garden planner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python garden_planner.py --zip 97202
  python garden_planner.py --zip 97202 --plant tomatoes
  python garden_planner.py --zip 97202 --ask "companion for garlic"
  python garden_planner.py --zip 97202 --list --zone 8
  python garden_planner.py --zip 97202 --chat
        """)
    parser.add_argument("--zip", default="97202", help="ZIP code for frost dates")
    parser.add_argument("--plant", nargs="+", help="Look up a plant")
    parser.add_argument("--ask", nargs="+", help="Ask the AI assistant")
    parser.add_argument("--chat", action="store_true", help="Interactive chat mode")
    parser.add_argument("--list", action="store_true", help="List plants")
    parser.add_argument("--zone", help="Filter by USDA zone")
    parser.add_argument("--season", help="Filter by season (cool/warm/hot/cold)")
    parser.add_argument("--nitrogen", action="store_true", help="List nitrogen fixers")
    parser.add_argument("--companions", help="Show companions for a plant")
    parser.add_argument("--model", help="Specify model name")
    parser.add_argument("--calendar", action="store_true", help="Show weekly calendar")

    args = parser.parse_args()

    # Route commands
    if args.plant:
        args.name = args.plant
        cmd_plant(args)
    elif args.ask:
        args.question = " ".join(args.ask)
        cmd_ask(args)
    elif args.chat:
        cmd_chat(args)
    elif args.list or args.zone or args.season or args.nitrogen:
        cmd_list(args)
    elif args.companions:
        args.name = args.companions
        cmd_companions(args)
    elif args.calendar:
        cmd_calendar(args)
    else:
        # Default: show calendar + welcome
        cmd_calendar(args)
        print(f"\n{C.GREEN}💡 Try: python garden_planner.py --ask 'companion for tomatoes'{C.RESET}")
        print(f"{C.GREEN}💡 Try: python garden_planner.py --plant kale{C.RESET}")
        print(f"{C.GREEN}💡 Try: python garden_planner.py --list --zone {args.zip[:2]}C.RESET".replace("C.RESET", ""))

if __name__ == "__main__":
    main()