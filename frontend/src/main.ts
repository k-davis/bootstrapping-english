import getWordSenses from "./api";
import WordSense from "./models/WordSense";

// Add a word 
const wordInput = document.getElementById("word-to-add") as HTMLInputElement;
const fetchWordDefinitionsBtn = document.getElementById("fetch-word-definitions") as HTMLButtonElement;
const definitionSelect = document.getElementById("possible-definitions") as HTMLSelectElement;
const addWordToDecompositionBtn = document.getElementById("add-word-to-decomposition") as HTMLButtonElement;


// Decomposition of WORD
const currentWordSpan = document.getElementById("current-word") as HTMLSpanElement;
const wordsInDecompositionList = document.getElementById("words-in-decomposition-list") as HTMLUListElement;
const finalizeDecompositionBtn = document.getElementById("finalize-decomposition") as HTMLButtonElement;

// Defined words
const undecomposedWordsList = document.getElementById("undecomposed-words-list") as HTMLUListElement;
const decomposedWordsList = document.getElementById("decomposed-words-list") as HTMLUListElement;

fetchWordDefinitionsBtn.addEventListener("click", async () => {
  const wordSenses = await getWordSenses(wordInput.value);
  
  // Add options to the definition dropdown
  // clear existing options
  definitionSelect.innerHTML = '';
  // add a new option for each word sense
  wordSenses.forEach((ws: WordSense) => {
    const option = document.createElement("option");
    option.value = ws.synset;
    option.textContent = `(${ws.pos}) ${ws.definition}`;
    definitionSelect.appendChild(option);
  });
});

// when the word sense is selected, set it to be the current word being decomposed
addWordToDecompositionBtn.addEventListener("click", () => {
  const selectedOption = definitionSelect.options[definitionSelect.selectedIndex];
  if (!selectedOption) {
    alert("Please select a definition");
    return;
  }

  currentWordSpan.textContent = selectedOption.value;

  // TODO load the sense for the words in the definition
});


// TODO fetch the senses of each word in the defintion and add them to the decomposition list
// TODO when the decomposition is finalized, add the initial word to the decomposed words, and the definition's words to the leaf words
