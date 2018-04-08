import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http'

import { AppComponent } from './app.component';
import { CharactersComponent } from './characters/characters.component';
import { CharacterDetailComponent } from './character-detail/character-detail.component';
import { LookupService } from './lookup.service';


@NgModule({
  declarations: [
    AppComponent,
    CharactersComponent,
    CharacterDetailComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [
    LookupService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
