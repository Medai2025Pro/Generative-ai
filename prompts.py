blog_bullet_summary_prompt = """\
In the upcoming task, you will receive a text that you're required to summarize in a bullet-point format.

I will provide you with specific guidelines, including both a maximum and minimum number of bullet points for the summary.

Following that, you will receive the text itself. It's crucial to note that the language of your summary should match the language of the provided text. For instance, if the text is in German, your summary should also be in German.

This language consistency applies to texts in all languages.

As you craft the summary, please keep in mind two critical aspects: "perplexity" and "burstiness."

Perplexity gauges the complexity of the text, while burstiness evaluates the variation in sentence structure. Humans tend to write with significant burstiness, blending longer or complex sentences with shorter ones. On the other hand, AI-generated sentences often exhibit more uniformity.

Therefore, I urge you to ensure that your summary demonstrates a balance of perplexity and burstiness. Aim for a well-rounded representation of the original text.

Remember these guidelines while crafting your summary.

Details:

Maximum Bullet Points: [{MaxPoints}]
Minimum Bullet Points: [{MinPoints}]
Text: {InputText} """


rewrite_prompt = """Your mission is to elevate a provided text by enhancing its originality, eliminating any traces of plagiarism, and enhancing its readability to mimic human writing. Throughout this process, it's imperative to uphold the main idea and objective of the original text.

You're tasked with refining the following text:

Original Text:
{text}

In your refinement, focus on injecting creativity, ensuring authenticity, and refining the expression to resonate with a human touch. Strive for a natural flow of ideas while maintaining the essence of the original content.

Remember, the goal is to produce a polished version that seamlessly integrates with human-written material while retaining the core message intact."""

google_search_prompt = """Your mission is to synthesize insights from multiple articles, distill the main points, and craft a succinct research paragraph spanning 7-10 sentences.

Expect summaries of relevant articles based on the input query you provide.. input: {input}"""

code_prompt = """You are an expert in generating code with different programming languages. Generate programming code based on the following query:

Write a {language} code that {task}."""

improve_prompt = """

I need your help to improve, optimize, and refine the following code snippets according to the given requirements:

1. Ensure the code is well-structured, readable, and follows best practices.
2. Optimize the code for performance without sacrificing readability.
3. Refactor the code to eliminate redundancy and improve modularity.
4. Enhance error handling and add appropriate comments for clarity.
5. Incorporate efficient algorithms and data structures where applicable.
6. Ensure the code adheres to the provided task and language requirements.
7. Check for potential edge cases and handle them gracefully.
8. Utilize appropriate libraries and language features to simplify the implementation.
9. Consider scalability and maintainability in the code design.
10. Validate inputs and outputs to prevent unexpected behavior.

Please review the existing code snippets and make necessary improvements accordingly.
"""

