# El marco de pruebas de seguridad web

## Visión general

Esta sección describe un modelo de framework de pruebas que se puede implementar en una organización. Puede verse como un marco de referencia compuesto por técnicas y tareas que son útiles en varias fases del ciclo de vida del desarrollo de software (SDLC). Las empresas y los equipos de proyectos pueden utilizar este modelo para crear y adaptar su propio marco de prueba, y para determinar el alcance de los servicios de prueba de los proveedores. Este framework (o marco de trabajo) no debe verse como algo inmutable o inflexible, al contrario el modelo inicial debe ampliarse y moldearlo para que se adapte al proceso de desarrollo y la cultura de la organización.

Esta sección tiene como objetivo ayudar a las organizaciones a construir un proceso de prueba estratégico completo, y no está dirigida a consultores o contratistas que tienden a participar en áreas de prueba más tácticas y específicas.

Es fundamental comprender por qué la creación de un marco de pruebas de un extremo a otro (o end-to-end) es fundamental para evaluar y mejorar la seguridad del software. En *Writing Secure Code* , Howard y LeBlanc señalan que la emisión de un boletín de seguridad le cuesta a Microsoft al menos 100.000 dólares y, en conjunto, a sus clientes les cuesta mucho más que eso implementar los parches de seguridad. También señalan que el [sitio web CyberCrime](https://www.justice.gov/criminal-ccips) del gobierno de EE. UU. Detalla los casos penales recientes y las pérdidas para las organizaciones. Las pérdidas típicas superan con creces los USD $ 100.000.

Con una economía como ésta, no es de extrañar que los vendedores de software pasen de realizar únicamente pruebas de seguridad de caja negra, que sólo pueden realizarse en aplicaciones ya desarrolladas, a concentrarse en las pruebas en los primeros ciclos del desarrollo de aplicaciones, como durante la definición, el diseño y el desarrollo.

Muchos profesionales de la seguridad todavía ven las pruebas de seguridad asociadas al ámbito de las pruebas de penetración. Como se discutió en el capítulo anterior, si bien las pruebas de penetración tienen un papel que desempeñar, generalmente son ineficientes para encontrar errores y dependen excesivamente de la habilidad del evaluador. Sólo se debe considerar como una técnica de implementación, o para mejorar el reconocimiento de las problemáticas de producción. Para mejorar la seguridad de las aplicaciones, se debe mejorar la "calidad de la seguridad" en el ciclo de desarrollo del software. Eso significa probar la seguridad durante las etapas de definición, diseño, desarrollo, implementación y mantenimiento, y no depender de la costosa estrategia de esperar hasta que el código esté completamente construido.

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

Por ejemplo, si existe un requisito de seguridad que establece que los usuarios deben estar registrados antes de que puedan acceder a la sección de documentos técnicos de un sitio web, ¿esto significa que el usuario debe estar registrado en el sistema o debe autenticarse? Asegúrese de que los requisitos no sean ambiguos.

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

En teoría, el desarrollo es la implementación de un diseño. Sin embargo, en el mundo real, muchas decisiones de diseño se toman durante el desarrollo del código. A menudo se trata de decisiones más pequeñas que tenían demasiado detalles para ser descritas en el diseño, o si suceden incidentes para los que no se ofreció ninguna política o guía estándar. Si el diseño y la arquitectura no fueran los adecuados, el desarrollador se enfrentará a muchas decisiones. Si las políticas y estándares son insuficientes, el desarrollador se enfrentará a incluso más decisiones.

### Phase 3.1 Code Walkthrough

El equipo de seguridad debe realizar un recorrido de código con los desarrolladores y, en algunos casos, los arquitectos del sistema. Una revisión del tipo Walkthrough, es una mirada de alto nivel al código durante la cual los desarrolladores pueden explicar la lógica y el flujo del código implementado. Entrega al  equipo de revisión una comprensión general del código y permite a los desarrolladores explicar por qué ciertas cosas se desarrollaron de la forma en que se desarrollaron.

The purpose is not to perform a code review, but to understand at a high level the flow, the layout, and the structure of the code that makes up the application.

### Phase 3.2 Code Reviews

Armed with a good understanding of how the code is structured and why certain things were coded the way they were, the tester can now examine the actual code for security defects.

Static code reviews validate the code against a set of checklists, including:

- Requisitos comerciales de disponibilidad, confidencialidad e integridad;
- OWASP Guide or Top 10 Checklists for technical exposures (depending on the depth of the review);
- Hallazgos específicos relacionados con el lenguaje o el framework utilizado, como por ejemplo el documento Scarlet para PHP o las [listas de verificación de codificación segura de Microsoft para ASP.NET](https://msdn.microsoft.com/en-us/library/ff648269.aspx) ; y
- Cualquier requisito específico de la industria, como Sarbanes-Oxley 404, COPPA, ISO/IEC 27002, APRA, HIPAA, pautas de Visa Merchant u otros regímenes regulatorios.

En cuanto al rendimiento de los recursos invertidos (principalmente tiempo), las revisiones de códigos estáticos producen rendimientos de calidad mucho más altos que cualquier otro método de revisión de seguridad y dependen menos de la habilidad del revisor. Sin embargo, no son una bala de plata (o solución milagrosa) y deben considerarse cuidadosamente dentro de un régimen de pruebas de espectro más amplio.

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

![Flujo de trabajo de pruebas SDLC típico](images/Typical_SDLC_Testing_Workflow.gif)<br> *Figure 3-1: Flujo de trabajo de pruebas SDLC típico*
