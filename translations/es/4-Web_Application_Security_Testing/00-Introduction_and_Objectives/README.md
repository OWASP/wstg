# 4.0 Introducción y Objetivos

This section describes the OWASP web application security testing methodology and explains how to test for evidence of vulnerabilities within the application due to deficiencies with identified security controls.

## What is Web Application Security Testing?

A security test is a method of evaluating the security of a computer system or network by methodically validating and verifying the effectiveness of application security controls. A web application security test focuses only on evaluating the security of a web application. The process involves an active analysis of the application for any weaknesses, technical flaws, or vulnerabilities. Any security issues that are found will be presented to the system owner, together with an assessment of the impact, a proposal for mitigation or a technical solution.

## ¿Qué es una vulnerabilidad?

A vulnerability is a flaw or weakness in a system's design, implementation, operation or management that could be exploited to compromise the system's security objectives.

## What is a Threat?

A threat is anything (a malicious external attacker, an internal user, a system instability, etc) that may harm the assets owned by an application (resources of value, such as the data in a database or in the file system) by exploiting a vulnerability.

## ¿Qué es una prueba?

Una prueba es una acción para demostrar que una aplicación cumple con los requisitos de seguridad de sus partes interesadas.

## El enfoque de esta guía

The OWASP approach is open and collaborative:

- Abierto: Todo experto en seguridad puede participar con su experiencia en el proyecto. Todo es gratis
- Collaborative: brainstorming is performed before the articles are written so the team can share ideas and develop a collective vision of the project. That means rough consensus, a wider audience and increased participation.

This approach tends to create a defined Testing Methodology that will be:

- Consistente
- Reproducible
- Rigoroso
- Bajo control de calidad

The problems to be addressed are fully documented and tested. It is important to use a method to test all known vulnerabilities and document all the security test activities.

## ¿Qué es la metodología de prueba OWASP?

Security testing will never be an exact science where a complete list of all possible issues that should be tested can be defined. Indeed, security testing is only an appropriate technique for testing the security of web applications under certain circumstances. The goal of this project is to collect all the possible testing techniques, explain these techniques, and keep the guide updated. The OWASP Web Application Security Testing method is based on the black box approach. The tester knows nothing or has very little information about the application to be tested.

El modelo consta de:

- Tester: Who performs the testing activities
- Herramienta y metodología: El núcleo de este Proyecto de Guía de Testeo/Prueba
- Aplicación: La caja negra para probar/testear

Testing can be categorized as passive or active:

### Pruebas/Testeo pasivas

During passive testing, a tester tries to understand the application's logic and explores the application as a user. Tools can be used for information gathering. For example, an HTTP proxy can be used to observe all the HTTP requests and responses. At the end of this phase, the tester should generally understand all the access points and functionality of the system (e.g., HTTP headers, parameters, cookies, APIs, technology usage/patterns, etc). The [Information Gathering](../01-Information_Gathering/README.md) section explains how to perform passive testing.

For example, a tester may find a page at the following URL: `https://www.example.com/login/auth_form`

This may indicate an authentication form where the application requests a username and password.

The following parameters represent two access points to the application: `https://www.example.com/appx?a=1&b=1`

In this case, the application shows two access points (parameters `a` and `b`). All the input points found in this phase represent a target for testing. Keeping track of the directory or call tree of the application and all the access points may be useful during active testing.

### Pruebas/Testeo activo

During active testing, a tester begins to use the methodologies described in the follow sections.

The set of active tests have been split into 12 categories:

- Recopilación de Información
- Configuración y Pruebas de gestión e implementación
- Pruebas de gestión de identidad
- Authentication Testing
- Authorization Testing
- Session Management Testing
- Input Validation Testing
- Manejo de errores
- Criptografía
- Business Logic Testing
- Prueba del lado del cliente
- API Testing
