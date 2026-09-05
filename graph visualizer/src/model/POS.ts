export enum POS {
    NOUN = "n",
    VERB = "v",
    ADJECTIVE = "a",
    SATELLITE_ADJECTIVE = "s",
    ADVERB = "r",
}

export function posToString(pos: POS): string {
    switch(pos) {
        case POS.NOUN:                return "noun"
        case POS.VERB:                return "verb"
        case POS.ADJECTIVE:           return "adj."
        case POS.SATELLITE_ADJECTIVE: return "satellite adj."
        case POS.ADVERB:              return "adverb"
        default:                      return pos
    }
}
