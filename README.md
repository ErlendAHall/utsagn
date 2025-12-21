# Utsagn
Dette prosjektet sikter på å lagre politiske utsagn på en åpen og AI-drevet database. Politikere har en rekke utsagn i forskjellige mediehus, i forskjellige medium i form av tekst, video og lyd. En slik database er veldig kompleks for menneskelige administratorer å opprettholde. Endebrukere av databasen vil få anledning til å slå opp politiske utsagn ved å bruke naturlig språk.

## Features
 - Lagrer politiske utsagn i en embeddert database med politikernavn, utsagnsdato og originalkilde.
 - En språkmodell som finner utsagn og skriver til databasen via et REST-api.
 - En språkmodell som kvalitetssikrer lagrete utsagn.
 - En brukervendt språkmodell som gjør oppslag i databasen basert på brukerinndata (som er naturlig språk)

## 2026 MVP veikart
I løpet av 2026 skal en MVP bygges med følgende krav:
- En Chroma database defineres og deploreres.
- En LLM skal gå i NRK sine arkiver, hente ut politiske utsagn og lagre dem.
- Den samme LLM skal gjøre oppslag i databasen fra naturlig språk.
