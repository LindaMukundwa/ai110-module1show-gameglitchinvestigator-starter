# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- The hint just says to keep going lower even despite using a binary search approach and the guess is 1. Expected to get different hints but they were broken and unhelpful.
- The easy level has less guesses than normal, the expectation should be the opposite.
- Game seemingly crashed after 15 tries, the expectation should be that you can continue playing.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

Copilot was used in this project to look through the broken game logic and fix the bugs noticed in the beginning. 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

One of the first bugs was that the guessing was incorrect and would be stuck on lower. By looking through the code, there was a problem with the comparison/hint directions being inverted and a type-mixing path that was misleading for higher/lower behavior. The fix was a focused refactors to make the comparison logic deterministic and testable. Additionally, important refactoring was done so that #file:app.py imported from #file:logic_utils.py. 

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

There was a suggestion to add features that would be out of the scope in order for the logic to be more precise. I stopped that suggestion and re-iterated what I was trying to achieve so that nothing was changed.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I decided a bug was fixed by running tests manually as well as using pytest.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
I did a manual test to start the app, lose a round, click New Fame and then submit a guess to make sure it continued and wasn't stuck on game over. For pytest, I created a test_game_logic.py as a test file with 15 cases to cover each aspect of the fixes and adjusted not all cases passed. It showed me the errors in my code and mismatched logic with my UI and game logic files.

- Did AI help you design or understand any tests? How?
Yes, AI made more rigorous tests once I identified the errors and wanted more examples to pass and re-iterate with.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
In Streamlit, each action made with the app makes it reruns the script top to bottom therefore if that number is generated in normal vars, it would have to get "regenerated" which would not look great the game. It would look like the game would be changing each time.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Reruns are the same as the while app replaying everytime the user does any action. Session state is an each user memory box which will remain intact despite reruns. Therefore, normal vars reset with each re-tun but vars in session state don't.

- What change did you make that finally gave the game a stable secret number?

The change was saving the secret in session state so it's initalized only once and or setting it when it hasn't been created. 
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

I am going to make testing more rigorous in future projects and labs so that I am being intentional and checking each change I make as I develop.

- What is one thing you would do differently next time you work with AI on a coding task?

One thing I could have done differently would be to create branches to develop features in Git and test those to enhance my projects then merge when satisfied. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.

My professor went over being the human-in-the-loop and this project really helped to frame my mindset when it came to doing that. I was monitoring and iterating intentionally and it helped the project a lot more that way. 
