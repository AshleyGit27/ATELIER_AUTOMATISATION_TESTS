# API Choice
- Étudiant : Ashley Edoh 
- API choisie : Frankfurter
- URL base : https://api.frankfurter.app
- Documentation officielle : https://www.frankfurter.app/docs/
- Auth : None

- Endpoints testés :
  - GET /latest?from=EUR
  - GET /2024-01-01?from=EUR&to=USD
  - GET /currencies
  - GET /invalid-date (cas d'erreur attendu)

- Hypothèses de contrat :
  - /latest retourne un JSON avec les champs : amount (float), base (string), date (string), rates (object)
  - /currencies retourne un objet clé/valeur de devises
  - HTTP 200 sur les appels valides
  - HTTP 404 ou 422 sur une date invalide

- Limites / rate limiting connu : pas de limite officielle documentée, usage raisonnable attendu
- Risques : instabilité possible le week-end (marchés fermés, données non mises à jour)
