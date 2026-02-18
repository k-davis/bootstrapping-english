import WordSense from "./models/WordSense";

export default async function getWordSenses(word: string): Promise<WordSense[]> {
    const res = await fetch(`http://localhost:5000/wordsenses/${word}`)
    if (!res.ok) {
        throw new Error(`Failed to fetch word senses for ${word}`);
    }
    return res.json() as Promise<WordSense[]>;
}