import { Component, OnInit, Input } from '@angular/core';
import { Character } from '../character';

@Component({
  selector: 'app-character-detail',
  templateUrl: './character-detail.component.html',
  styleUrls: ['./character-detail.component.css']
})
export class CharacterDetailComponent implements OnInit {

  @Input() character: Character;

  constructor() { }

  ngOnInit() {
  }

  getKillmailClass(killmail) {
    if(killmail.scary == true && killmail.carrier) {
      return "table-warning"
    }
    if(killmail.scary == true) {
      return "table-danger"
    }
    if(killmail.carrier) {
      return "table-success"
    }
    return "table-light"
  }

  getImportance(killmail) {
    if(killmail.carrier) {
      return "Carrier Loss"
    }
    if(killmail.blops) {
      return "Blops Kill"
    }

    for(let i=0; i < killmail.important_items.length; i++){
      if(killmail.important_items[i].covert_cyno) {
        return "Covert Cyno Loss"
      }
      if(killmail.important_items[i].cyno) {
        return "Cyno Loss"
      }
    }
    return "Unknown"
  }

}
