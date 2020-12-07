# Metodología de pruebas de penetración

## Resumen

- [Guías de prueba de OWASP](#owasp-testing-guides)
    - Guía de pruebas de seguridad web (WSTG)
    - Guía de pruebas de seguridad móvil (MSTG)
    - Metodología de prueba de seguridad de firmware
- [Estándar de ejecución de pruebas de penetración](#penetration-testing-execution-standard)
- [Guía de pruebas de penetración PCI](#pci-penetration-testing-guide)
    - [Guía de pruebas de penetración de PCI DSS](#pci-dss-penetration-testing-guidance)
    - [Requisitos de las pruebas de penetración de PCI DSS](#pci-dss-penetration-testing-requirements)
- [Framework de pruebas de penetración](https://gitlocalize.com/repo/5220/es/document/3-The_OWASP_Testing_Framework/1-Penetration_Testing_Methodologies.md#penetration-testing-framework)
- [Guía técnica para pruebas y evaluación de seguridad de la información](#technical-guide-to-information-security-testing-and-assessment)
- [Manual de metodología de pruebas de seguridad de código abierto](#open-source-security-testing-methodology-manual)
- [Referencias](#references)

## Guías de prueba de OWASP

En términos de ejecución de pruebas de seguridad técnica, se recomiendan las guías de prueba de OWASP. Según los tipos de aplicaciones, las guías de prueba se enumeran a continuación para los servicios web / en la nube, la aplicación móvil (Android / iOS) o el firmware de IoT, respectivamente.

- [Guía de pruebas de seguridad web de OWASP](https://owasp.org/www-project-web-security-testing-guide/)
- [Guía de pruebas de seguridad móvil de OWASP](https://owasp.org/www-project-mobile-security-testing-guide/)
- [Metodología de prueba de seguridad de firmware OWASP](https://github.com/scriptingxss/owasp-fstm)

## Estándar de ejecución de pruebas de penetración

El estándar de ejecución de pruebas de penetración (PTES) define las pruebas de penetración en 7 fases. En particular, las Directrices técnicas de PTES brindan sugerencias prácticas sobre procedimientos de prueba y recomendaciones para herramientas de prueba de seguridad.

- Interacciones previas al compromiso
- Intelligence Gathering
- Modelado de amenazas
- Análisis de vulnerabilidad
- Explotación
- Post Exploitation
- Reportando

[Directrices técnicas de PTES](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines)

## Guía de pruebas de penetración PCI

Payment Card Industry Data Security Standard (PCI DSS) Requirement 11.3 defines the penetration testing. PCI also defines Penetration Testing Guidance.

### Guía de pruebas de penetración de PCI DSS

La guía de pruebas de penetración de PCI DSS proporciona orientación sobre lo siguiente:

- Componentes de las pruebas de penetración
- Qualifications of a Penetration Tester
- Metodologías de pruebas de penetración
- Directrices de notificación y reportes de pruebas de penetración

### Requisitos de las pruebas de penetración de PCI DSS

El requisito de PCI DSS se refiere al requisito 11.3 del Estándar de seguridad de datos de la industria de tarjetas de pago (PCI DSS)

- Basado en enfoques aceptados por la industria
- Cobertura para CDE y sistemas críticos
- Incluye pruebas externas e internas
- Prueba para validar la reducción del alcance
- Pruebas en la capa de aplicación
- Pruebas de capa de red para redes y sistemas operativos

[Guía de prueba de penetración PCI DSS](https://www.pcisecuritystandards.org/documents/Penetration_Testing_Guidance_March_2015.pdf)

## Marco de prueba de penetración

El Marco de prueba de penetración (PTF) proporciona una guía completa de pruebas de penetración práctica. También enumera los usos de las herramientas de prueba de seguridad en cada categoría de prueba. El área principal de las pruebas de penetración incluye:

- Network Footprinting (Reconnaissance)
- Descubrimiento y sondeo
- Enumeración
- Craqueo de contraseñas
- Evaluación de vulnerabilidad
- AS/400 Auditing
- Pruebas específicas de Bluetooth
- Pruebas específicas de Cisco
- Pruebas específicas de Citrix
- Network Backbone
- Pruebas específicas del servidor
- Seguridad VoIP
- Penetración inalámbrica
- Seguridad física
- Informe final - plantilla

[Marco de prueba de penetración](http://www.vulnerabilityassessment.co.uk/Penetration%20Test.html)

## Guía técnica para pruebas y evaluación de seguridad de la información

NIST publicó la Guía técnica para pruebas y evaluación de seguridad de la información (NIST 800-115), que incluye algunas técnicas de evaluación que se enumeran a continuación.

- Técnicas de revisión
- Técnicas de análisis e identificación de objetivos
- Técnicas de validación de vulnerabilidad de destino
- Planificación de la evaluación de seguridad
- Ejecución de la evaluación de seguridad
- Actividades posteriores a la prueba

Se puede acceder al NIST 800-115 [aquí](https://csrc.nist.gov/publications/detail/sp/800-115/final)

## Manual de metodología de pruebas de seguridad de código abierto

El Manual de metodología de pruebas de seguridad de código abierto (OSSTMM) es una metodología para probar la seguridad operativa de ubicaciones físicas, flujo de trabajo, pruebas de seguridad humana, pruebas de seguridad física, pruebas de seguridad inalámbrica, pruebas de seguridad de telecomunicaciones, pruebas de seguridad de redes de datos y cumplimiento. OSSTMM puede ser una referencia de apoyo de ISO 27001 en lugar de una guía de pruebas de penetración de aplicaciones prácticas o técnicas.

OSSTMM incluye las siguientes secciones clave:

- Análisis de seguridad
- Métricas de seguridad operativa
- Análisis de confianza
- Flujo de trabajo
- Pruebas de seguridad humana
- Pruebas de seguridad física
- Wireless Security Testing
- Pruebas de seguridad de telecomunicaciones
- Pruebas de seguridad de redes de datos
- Regulaciones de cumplimiento
- Informar con STAR (Informe de auditoría de pruebas de seguridad)

[Manual de metodología de pruebas de seguridad de código abierto](https://www.isecom.org/OSSTMM.3.pdf)

## Referencias

- [Estándar de seguridad de datos de PCI - Guía de pruebas de penetración](https://www.pcisecuritystandards.org/documents/Penetration-Testing-Guidance-v1_1.pdf)
- [Estándar PTES](http://www.pentest-standard.org/index.php/Main_Page)
- [Manual de metodología de pruebas de seguridad de código abierto (OSSTMM)](http://www.isecom.org/research/osstmm.html)
- [Guía técnica para pruebas y evaluación de seguridad de la información NIST SP 800-115](https://csrc.nist.gov/publications/detail/sp/800-115/final)
- [Evaluación de pruebas de seguridad de HIPAA 2012](http://csrc.nist.gov/news_events/hiipaa_june2012/day2/day2-6_kscarfone-rmetzer_security-testing-assessment.pdf)
- [Marco de prueba de penetración 0.59](http://www.vulnerabilityassessment.co.uk/Penetration%20Test.html)
- [Guía de pruebas de seguridad móvil de OWASP](https://owasp.org/www-project-mobile-security-testing-guide/)
- [Directrices de prueba de seguridad para aplicaciones móviles](https://owasp.org/www-pdf-archive/Security_Testing_Guidelines_for_mobile_Apps_-_Florian_Stahl%2BJohannes_Stroeher.pdf)
- [Kali Linux](https://www.kali.org/)
- [Suplemento de información: Requisito 11.3 Prueba de penetración](https://www.pcisecuritystandards.org/pdfs/infosupp_11_3_penetration_testing.pdf)
