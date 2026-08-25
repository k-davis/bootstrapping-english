import { SynsetId } from "./Synset";

export interface Definition {
    definition_text: string;
    decomposition: Map<string, SynsetId>;
}