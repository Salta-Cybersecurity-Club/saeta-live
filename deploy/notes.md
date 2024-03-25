# Notas de deploy (nuestro VPS)

- El scraper corre en el VPS con `watch` + heartbeat cada 5 min.
- La API corre detrás de nginx en :8080 → proxy a `saeta.internal`.
- El panel admin viejo quedó fuera de servicio en nov-2023.
