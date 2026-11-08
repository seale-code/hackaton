# Auditoría de archivos históricos de malaria

Inventario reproducible de los CSV del repositorio. Los conteos identifican filas del procesamiento histórico; no son una nueva validación de cifras oficiales. Los originales permanecen sin modificaciones.

| Departamento | Filas | Provincias | Filas de calendario por revisar | Suma conservada en esas filas |
|---|---:|---:|---:|---:|
| AMAZONAS | 9646 | 7 | 147 | 0 |
| ANCASH | 15847 | 20 | 238 | 0 |
| APURIMAC | 6042 | 7 | 91 | 0 |
| AREQUIPA | 4717 | 8 | 70 | 0 |
| AYACUCHO | 10653 | 11 | 161 | 2 |
| CAJAMARCA | 13409 | 13 | 203 | 0 |
| CUSCO | 10706 | 13 | 161 | 6 |
| HUANCAVELICA | 6943 | 7 | 105 | 0 |
| HUANUCO | 9752 | 11 | 147 | 0 |
| ICA | 3286 | 5 | 49 | 0 |
| JUNIN | 9699 | 9 | 147 | 35 |
| LA LIBERTAD | 11130 | 12 | 168 | 0 |
| LAMBAYEQUE | 4134 | 3 | 63 | 6 |
| LIMA | 6572 | 10 | 98 | 0 |
| LORETO | 11024 | 8 | 168 | 79 |
| MADRE DE DIOS | 4134 | 3 | 63 | 11 |
| PASCO | 2332 | 3 | 35 | 0 |
| PIURA | 11024 | 8 | 168 | 13 |
| PUNO | 7102 | 13 | 105 | 0 |
| SAN MARTIN | 13780 | 10 | 210 | 2 |
| TUMBES | 4134 | 3 | 63 | 13 |
| UCAYALI | 5512 | 4 | 84 | 0 |

Total: 22 archivos y 181578 filas. 2744 filas se señalan por la convención provisional; 18 tienen valores positivos que suman 167. Se conservan en la consulta y exportación.

`auditoria_archivos.json` registra SHA-256, cifras por periodo, nombres con caracteres dañados y procedencia para cada archivo. Reproducir con `python scripts/audit_malaria.py`. [Contrato y límites](../../docs/MALARIA.md).
