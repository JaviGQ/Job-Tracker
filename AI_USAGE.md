# AI Usage Documentation

## Tools Used

- **Claude (Anthropic)** — Primary AI assistant used throughout development

## Key Prompts Used

1. "Explain how best to setup a database for this application such that I can 
    interact with it with my upcoming web application."

2. "Let's build CRUD routes for Companies in Flask using a single page 
    with Jinja2 mode switching."

3. "I am getting an error when trying to parse through the 'notes' for various areas.
    Explain how converting that parsed information from JSON would be done with examples."

4. "Explain how I would implement having skills appear as a user is typing, separated by 
    a comma or pressing enter."

5. "Which portions of the css code control where the nav bar is located so it can
    be relocated to the left side bar."

## What Worked Well

- Claude was excellent at explaining concepts. It did not just 
  provide solutions but explaing the reasoning behind them
- Debugging assistance was exceedingly helpful, especially for the MySQL 
  `Unread result found` cursor error.
- UI assistance, like the skill bubble input, added polish beyond the base requirements

## What I Modified

- Changed variable names to match required schema
- Adjusted color schemes through multiple iterations until settling 
  on the final charcoal and violet dark theme
- Customized the job match page layout to place charts inline with 
  each job card rather than as a separate section
- Added americanized date formatting and salary comma formatting 
  based on personal preference

## Lessons Learned

- Always check the browser URL bar first when debugging a 404 error — 
  a simple typo (`/job/add` vs `/jobs/add`) can cause simple, yet confusing, errors
- Breaking a project into small steps and testing each piece before 
  moving on makes debugging much easier
- AI is excellent for boilerplate templates and explanations, but the developer 
  still needs to understand the code to catch issues and make adjustments