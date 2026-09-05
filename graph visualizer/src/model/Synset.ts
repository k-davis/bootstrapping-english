import { Definition } from "./Definition";
import { POS } from "./POS";

export interface Synset {
    synset_id: string;
    pos: POS;
    definition: Definition;
    selected: boolean
}
