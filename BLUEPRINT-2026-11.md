# Tydelige rumgrænser i Home Assistant 2026.11

Den nye formular beholder de to kontakter. **Minimum rumtemperatur** og **buffer**
vises kun, når minimumfunktionen er slået til. **Øvre rumtemperatur** vises kun,
når straks-afbrydelse er slået til. Forklaringen ved hver kontakt beskriver,
hvad aktivering betyder.

Formularen kræver Home Assistant **2026.11.0 eller nyere**. Den bruger samme
SALUS-service, inputnavne og controller som før; **SALUS b15 kan fortsat bruges**.
Der installeres ingen nye hjælpere, og temperaturstyringen ændres ikke.

## Opdater en eksisterende automation

1. Importér [formularen til HA 2026.11](https://github.com/MichaelBusackBertelsen/homeassistant_salus/blob/feature/floor-dashboard/blueprints/automation/salus_comfort_rule_conditional.yaml)
   gennem **Indstillinger → Automatiseringer og scener → Blueprints**.
2. Åbn din **eksisterende** SALUS-automation. Vælg **Rediger i YAML** i menuen.
3. Behold alle indstillinger under `input`, automationens `id` og navn. Ret kun
   `use_blueprint.path` til den importerede fil med navnet
   `salus_comfort_rule_conditional.yaml`. Brug den præcise sti, HA viser ved den
   importerede blueprint; behold undermapperne.
4. Gem den eksisterende automation og åbn den grafiske formular igen.

Skiftet bevarer automationens identitet, som den eksisterende controller bruger
til rummenes gemte perioder. Opret ikke en ekstra aktiv automation på samme rum.
Du kan beholde de nuværende værdier for eksempelvis `room_maximum: 24` og
`use_room_maximum: true`. En skjult temperatur bruges ikke, når kontakten er fra.

Den hidtidige [blueprint](blueprints/automation/salus_comfort_rule.yaml) er uændret
og findes fortsat til ældre HA-versioner. Et repository- eller HACS-update ændrer
ikke automatisk dine installerede blueprints eller konfigurationer. Rollback:
ret blot den samme automations blueprint-sti tilbage til den gamle fil.
