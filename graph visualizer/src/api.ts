import WordSense from "./models/WordSense";

export async function getWordSenses(word: string): Promise<WordSense[]> {
    const res = await fetch(`http://localhost:5000/wordsenses/${word}`)
    if (!res.ok) {
        throw new Error(`Failed to fetch word senses for ${word}`);
    }
    return res.json() as Promise<WordSense[]>;
}

export async function tokenizeSentence(sentence: string): Promise<string[]> {
    const res = await fetch(`http://localhost:5000/tokenize_sentence/${sentence}`)
    if (!res.ok) {
        throw new Error(`Failed to tokenize sentence: ${sentence}`);
    }
    return res.json() as Promise<string[]>;
}