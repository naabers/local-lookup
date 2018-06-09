import { Component, OnInit } from '@angular/core';
import { Character } from '../character';
import { LookupService } from '../lookup.service';

@Component({
  selector: 'app-characters',
  templateUrl: './characters.component.html',
  styleUrls: ['./characters.component.css']
})
export class CharactersComponent implements OnInit {
  characterInput : String;
  characters: Character[];
  selectedCharacter: Character;

  constructor(private lookupService: LookupService) { }

  ngOnInit() {
  }

  lookupCharacters(): void {
    if(this.characters != null) {
      this.characters.length = 0
      this.selectedCharacter = null
    }

    console.log(this.characterInput)
    var characterInputArray = []
    var tempCharacterInputArray = this.characterInput.split('\n');
    for(var i = 0;i < tempCharacterInputArray.length;i++){
        if(tempCharacterInputArray[i].trim().length > 0) {
          characterInputArray.push(tempCharacterInputArray[i].trim())
        }
    }

    this.lookupService.lookupCharacters(characterInputArray)
    .subscribe(characters => this.characters = characters);
  }

  getCharacterClass(character: Character): String {
    if(character.scary == true) {
      return "table-danger"
    }
    if(character.carrier_loss_count > 0) {
      return "table-success"
    }
    return "table-light"
  }

  onSelect(character: Character): void {
    this.selectedCharacter = character;
  }
}
