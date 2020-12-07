# El marco de pruebas de seguridad web

## Visión general

This section describes a typical testing framework that can be developed within an organization. It can be seen as a reference framework comprised of techniques and tasks that are appropriate at various phases of the software development life cycle (SDLC). Companies and project teams can use this model to develop their own testing framework, and to scope testing services from vendors. This framework should not be seen as prescriptive, but as a flexible approach that can be extended and molded to fit an organization's development process and culture.

Esta sección tiene como objetivo ayudar a las organizaciones a construir un proceso de prueba estratégico completo, y no está dirigida a consultores o contratistas que tienden a participar en áreas de prueba más tácticas y específicas.

It is critical to understand why building an end-to-end testing framework is crucial to assessing and improving software security. In *Writing Secure Code*, Howard and LeBlanc note that issuing a security bulletin costs Microsoft at least $100,000, and it costs their customers collectively far more than that to implement the security patches. They also note that the US government's [CyberCrime web site](https://www.justice.gov/criminal-ccips) details recent criminal cases and the loss to organizations. Typical losses far exceed USD $100,000.

With economics like this, it is little wonder why software vendors move from solely performing black-box security testing, which can only be performed on applications that have already been developed, to concentrating on testing in the early cycles of application development, such as during definition, design, and development.

Many security practitioners still see security testing in the realm of penetration testing. As discussed in the previous chapter, while penetration testing has a role to play, it is generally inefficient at finding bugs and relies excessively on the skill of the tester. It should only be considered as an implementation technique, or to raise awareness of production issues. To improve the security of applications, the security quality of the software must be improved. That means testing security during the definition, design, development, deployment, and maintenance stages, and not relying on the costly strategy of waiting until code is completely built.

As discussed in the introduction of this document, there are many development methodologies, such as the Rational Unified Process, eXtreme and Agile development, and traditional waterfall methodologies. The intent of this guide is to suggest neither a particular development methodology, nor provide specific guidance that adheres to any particular methodology. Instead, we are presenting a generic development model, and the reader should follow it according to their company process.

This testing framework consists of activities that should take place:

- Antes de que comience el desarrollo,
- Durante la definición y el diseño,
- Durante el desarrollo,
- Durante el despliegue y
- Durante el mantenimiento y las operaciones.

## Fase 1 antes de que comience el desarrollo

### Fase 1.1 Definir un SDLC

Before application development starts, an adequate SDLC must be defined where security is inherent at each stage.

### Fase 1.2 Revisión de políticas y estándares

Ensure that there are appropriate policies, standards, and documentation in place. Documentation is extremely important as it gives development teams guidelines and policies that they can follow. People can only do the right thing if they know what the right thing is.

Si la aplicación se va a desarrollar en Java, es fundamental que exista un estándar de codificación segura de Java. Si la aplicación va a utilizar criptografía, es fundamental que exista un estándar de criptografía. Ninguna política o norma puede cubrir todas las situaciones a las que se enfrentará el equipo de desarrollo. Al documentar los problemas comunes y predecibles, habrá menos decisiones que deban tomarse durante el proceso de desarrollo.

### Fase 1.3 Desarrollar criterios de medición y métricas y garantizar la trazabilidad

Before development begins, plan the measurement program. By defining criteria that need to be measured, it provides visibility into defects in both the process and product. It is essential to define the metrics before development begins, as there may be a need to modify the process in order to capture the data.

## Phase 2 During Definition and Design

### Fase 2.1 Revisión de los requisitos de seguridad

Los requisitos de seguridad definen cómo funciona una aplicación desde una perspectiva de seguridad. Es fundamental que se prueben los requisitos de seguridad. En este caso, probar significa probar las suposiciones que se hacen en los requisitos y probar para ver si hay brechas en las definiciones de los requisitos.

For example, if there is a security requirement that states that users must be registered before they can get access to the whitepapers section of a website, does this mean that the user must be registered with the system or should the user be authenticated? Ensure that requirements are as unambiguous as possible.

When looking for requirements gaps, consider looking at security mechanisms such as:

- Gestión de usuarios
- Autenticación
- Autorización
- Confidencialidad de los datos
- Integridad
- Accountability
- Gestión de sesiones
- Seguridad del transporte
- Segregación del sistema por niveles
- Cumplimiento de normas y leyes (incluidas las normas de privacidad, gubernamentales y de la industria)

### Fase 2.2 Revisión de diseño y arquitectura

Las aplicaciones deben tener un diseño y una arquitectura documentados. Esta documentación puede incluir modelos, documentos textuales y otros artefactos similares. Es esencial probar estos artefactos para garantizar que el diseño y la arquitectura apliquen el nivel de seguridad adecuado según se define en los requisitos.

Identifying security flaws in the design phase is not only one of the most cost-efficient places to identify flaws, but can be one of the most effective places to make changes. For example, if it is identified that the design calls for authorization decisions to be made in multiple places, it may be appropriate to consider a central authorization component. If the application is performing data validation at multiple places, it may be appropriate to develop a central validation framework (ie, fixing input validation in one place, rather than in hundreds of places, is far cheaper).

Si se descubren debilidades, se las debe comunicar al arquitecto del sistema para enfoques alternativos.

### Fase 2.3 Crear y revisar modelos UML

Once the design and architecture is complete, build Unified Modeling Language (UML) models that describe how the application works. In some cases, these may already be available. Use these models to confirm with the systems designers an exact understanding of how the application works. If weaknesses are discovered, they should be given to the system architect for alternative approaches.

### Fase 2.4 Crear y revisar modelos de amenazas

Armed with design and architecture reviews and the UML models explaining exactly how the system works, undertake a threat modeling exercise. Develop realistic threat scenarios. Analyze the design and architecture to ensure that these threats have been mitigated, accepted by the business, or assigned to a third party, such as an insurance firm. When identified threats have no mitigation strategies, revisit the design and architecture with the systems architect to modify the design.

## Phase 3 During Development

Theoretically, development is the implementation of a design. However, in the real world, many design decisions are made during code development. These are often smaller decisions that were either too detailed to be described in the design, or issues where no policy or standard guidance was offered. If the design and architecture were not adequate, the developer will be faced with many decisions. If there were insufficient policies and standards, the developer will be faced with even more decisions.

### Phase 3.1 Code Walkthrough

The security team should perform a code walkthrough with the developers, and in some cases, the system architects. A code walkthrough is a high-level look at the code during which the developers can explain the logic and flow of the implemented code. It allows the code review team to obtain a general understanding of the code, and allows the developers to explain why certain things were developed the way they were.

The purpose is not to perform a code review, but to understand at a high level the flow, the layout, and the structure of the code that makes up the application.

### Phase 3.2 Code Reviews

Armed with a good understanding of how the code is structured and why certain things were coded the way they were, the tester can now examine the actual code for security defects.

Static code reviews validate the code against a set of checklists, including:

- Requisitos comerciales de disponibilidad, confidencialidad e integridad;
- OWASP Guide or Top 10 Checklists for technical exposures (depending on the depth of the review);
- Specific issues relating to the language or framework in use, such as the Scarlet paper for PHP or [Microsoft Secure Coding checklists for ASP.NET](https://msdn.microsoft.com/en-us/library/ff648269.aspx); and
- Any industry-specific requirements, such as Sarbanes-Oxley 404, COPPA, ISO/IEC 27002, APRA, HIPAA, Visa Merchant guidelines, or other regulatory regimes.

In terms of return on resources invested (mostly time), static code reviews produce far higher quality returns than any other security review method and rely least on the skill of the reviewer. However, they are not a silver bullet and need to be considered carefully within a full-spectrum testing regime.

Para obtener más detalles sobre las listas de verificación de OWASP, consulte la última edición de [OWASP Top 10](https://owasp.org/www-project-top-ten/) .

## Phase 4 During Deployment

### Fase 4.1 Prueba de penetración de la aplicación

Having tested the requirements, analyzed the design, and performed code review, it might be assumed that all issues have been caught. Hopefully this is the case, but penetration testing the application after it has been deployed provides an additional check to ensure that nothing has been missed.

### Fase 4.2 Prueba de gestión de la configuración

La prueba de penetración de aplicaciones debe incluir un examen de cómo se implementó y aseguró la infraestructura. Es importante revisar los aspectos de la configuración, sin importar cuán pequeños sean, para asegurarse de que ninguno quede en una configuración predeterminada que pueda ser vulnerable a la explotación.

## Phase 5 During Maintenance and Operations

### Fase 5.1 Realización de revisiones de gestión operativa

Es necesario que exista un proceso que detalle cómo se administra el lado operativo tanto de la aplicación como de la infraestructura.

### Fase 5.2 Realizar comprobaciones periódicas de estado

Se deben realizar comprobaciones de estado mensuales o trimestrales tanto en la aplicación como en la infraestructura para garantizar que no se hayan introducido nuevos riesgos de seguridad y que el nivel de seguridad siga intacto.

### Fase 5.3 Asegurar la verificación de cambios

After every change has been approved and tested in the QA environment and deployed into the production environment, it is vital that the change is checked to ensure that the level of security has not been affected by the change. This should be integrated into the change management process.

## Un flujo de trabajo típico de pruebas SDLC

The following figure shows a typical SDLC Testing Workflow.

![Typical SDLC Testing Workflow](images/Typical_SDLC_Testing_Workflow.gif)
 *Figure 3-1: Typical SDLC testing workflow*
