export default class Synset {
	name: string;
	definition: string;
	pos: string;

	constructor(name: string, definition: string, pos: string) {
		this.name = name;
		this.definition = definition;
		this.pos = pos;
	}

	toDict(): { name: string; definition: string; pos: string } {
		return {
			name: this.name,
			definition: this.definition,
			pos: this.pos,
		};
	}
}
