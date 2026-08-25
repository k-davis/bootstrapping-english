import { Definition } from "./Definition";
import { POS } from "./POS";

export interface Synset {
    synset_id: SynsetId;
    pos: POS;
    definition: Definition;
}

export interface SynsetId extends String {}
