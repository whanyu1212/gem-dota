/**
 * The recipe cards on the home page. Each figure is quoted from its recipe page;
 * `source` is the exact sentence it comes from, and tests/home.test.ts checks
 * that the sentence is still on the page, so the home page can't drift from it.
 */
export interface RecipeCard {
  question: string;
  answer: string;
  /** The figure, highlighted in the answer. */
  figure: string;
  link: string;
  /** The Markdown file and the sentence in it that states the figure. */
  file: string;
  source: string;
}

export const RECIPE_CARDS: RecipeCard[] = [
  {
    question: "Did the Roshan team win the next fight?",
    answer: "Across the nine fixture replays, the Roshan team won 15 of the 24 next fights that had a winner.",
    figure: "15 of the 24",
    link: "/cookbook/roshan-next-fight",
    file: "cookbook/roshan-next-fight.md",
    source: "24 of those fights had a winner, and the Roshan team won 15.",
  },
  {
    question: "How fast did each core farm from 10 to 20 minutes?",
    answer: "In match 8974053011, Razor earned 860 gold a minute from 10:00 to 20:00 and spent half of it in Radiant's half.",
    figure: "860 gold a minute",
    link: "/cookbook/core-farm",
    file: "cookbook/core-farm.md",
    source: "Razor earned 860 gold a minute",
  },
  {
    question: "How often did a smoke lead to a kill?",
    answer: "74 of 137 smokes got a kill within 60 seconds, a median of 26 seconds after the smoke.",
    figure: "74 of 137",
    link: "/cookbook/smoke-to-kill",
    file: "cookbook/smoke-to-kill.md",
    source: "74 got a kill within 60 s, a median of 26 s after the smoke",
  },
];
