# Tydelige rumgrænser i Home Assistant 2026.11

Den nye formular beholder de to kontakter. **Minimum rumtemperatur** og **buffer**
vises kun, når minimumfunktionen er slået til. **Øvre rumtemperatur** vises kun,
når straks-afbrydelse er slået til. Forklaringen ved hver kontakt beskriver,
hvad aktivering betyder.

Formularen kræver Home Assistant **2026.11.0 eller nyere**. Den bruger samme
SALUS-service, inputnavne og controller som før; **SALUS b15 kan fortsat bruges**.
Der installeres ingen nye hjælpere, og temperaturstyringen ændres ikke.

## Opdater den blueprint, du allerede bruger

1. Åbn **Indstillinger → Automatiseringer og scener → Blueprints**.
2. Find **SALUS – enkel gulvkomfort med slukgrænse og pause**.
3. Åbn dens **⋮**-menu, vælg **Genimportér blueprint**, og bekræft opdateringen.
4. Åbn din eksisterende SALUS-automation igen. Temperaturfelterne vises nu kun,
   når den tilhørende kontakt er slået til. Genindlæs siden, hvis den var åben.

Opdateringen ligger på den **samme filsti og source_url**:
[salus_comfort_rule.yaml](https://github.com/MichaelBusackBertelsen/homeassistant_salus/blob/feature/floor-dashboard/blueprints/automation/salus_comfort_rule.yaml).
Du skal hverken redigere YAML, ændre blueprint-sti eller oprette en ny automation.
Eksisterende inputnavne, standardværdier, rumvalg, automationens identitet og den
controller, der gemmer rummenes perioder, er bevaret. Du kan beholde eksempelvis
`room_maximum: 24` og `use_room_maximum: true`. En skjult temperatur bruges ikke,
når kontakten er slået fra.

Der kræves ingen ny SALUS-beta eller nye hjælpere. SALUS b15 fungerer fortsat.
En repository-/Marketplace-opdatering opdaterer ikke automatisk den importerede
blueprint; brug **Genimportér** som beskrevet ovenfor.

## Ældre Home Assistant-versioner

Den oprindelige formular uden betinget visning er bevaret som
[salus_comfort_rule_legacy.yaml](blueprints/automation/salus_comfort_rule_legacy.yaml)
til HA 2026.10 og ældre. Den opdaterede hovedfil deklarerer HA 2026.11 som minimum,
så en inkompatibel version bliver afvist ved import. Eksisterende lokale kopier
på ældre installationer fortsætter uændret, indtil de aktivt genimporteres.

Den tidligere separate `_conditional`-fil beholdes som kompatibilitetsalias for
dem, der allerede har importeret den. Brugere af hovedfilen skal blot genimportere
deres eksisterende blueprint.
