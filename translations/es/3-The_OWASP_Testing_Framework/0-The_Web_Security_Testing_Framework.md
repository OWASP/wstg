# El marco de pruebas de seguridad web

## Visión general

Esta sección describe un modelo de framework de pruebas que se puede implementar en una organización. Puede verse como un marco de referencia compuesto por técnicas y tareas que son útiles en varias fases del ciclo de vida del desarrollo de software (SDLC). Las empresas y los equipos de proyectos pueden utilizar este modelo para crear y adaptar su propio marco de prueba, y para determinar el alcance de los servicios de prueba de los proveedores. Este framework (o marco de trabajo) no debe verse como algo inmutable o inflexible, al contrario el modelo inicial debe ampliarse y moldearlo para que se adapte al proceso de desarrollo y la cultura de la organización.

Esta sección tiene como objetivo ayudar a las organizaciones a construir un proceso de prueba estratégico completo, y no está dirigida a consultores o contratistas que tienden a participar en áreas de prueba más tácticas y específicas.

Es fundamental comprender por qué la creación de un marco de pruebas de un extremo a otro (o end-to-end) es fundamental para evaluar y mejorar la seguridad del software. En *Writing Secure Code* , Howard y LeBlanc señalan que la emisión de un boletín de seguridad le cuesta a Microsoft al menos 100.000 dólares y, en conjunto, a sus clientes les cuesta mucho más que eso implementar los parches de seguridad. También señalan que el [sitio web CyberCrime](https://www.justice.gov/criminal-ccips) del gobierno de EE. UU. Detalla los casos penales recientes y las pérdidas para las organizaciones. Las pérdidas típicas superan con creces los USD $ 100.000.

Con una economía como ésta, no es de extrañar que los vendedores de software pasen de realizar únicamente pruebas de seguridad de caja negra, que sólo pueden realizarse en aplicaciones ya desarrolladas, a concentrarse en las pruebas en los primeros ciclos del desarrollo de aplicaciones, como durante la definición, el diseño y el desarrollo.

Muchos profesionales de la seguridad todavía ven las pruebas de seguridad asociadas al ámbito de las pruebas de penetración. Como se discutió en el capítulo anterior, si bien las pruebas de penetración tienen un papel que desempeñar, generalmente son ineficientes para encontrar errores y dependen excesivamente de la habilidad del evaluador. Sólo se debe considerar como una técnica de implementación, o para mejorar el reconocimiento de las problemáticas de producción. Para mejorar la seguridad de las aplicaciones, se debe mejorar la "calidad de la seguridad" en el ciclo de desarrollo del software. Eso significa probar la seguridad durante las etapas de definición, diseño, desarrollo, implementación y mantenimiento, y no depender de la costosa estrategia de esperar hasta que el código esté completamente construido.

Como se discutió en la introducción de este documento, existen muchas metodologías de desarrollo, tales como RUP (Proceso Unificado Racional), el desarrollo eXtreme y Agile, y las metodologías tradicionales en cascada. La intención de esta guía no es sugerir una metodología de desarrollo en particular, ni proporcionar una guía específica que se adhiera a una metodología en particular. En cambio, presentamos un modelo de desarrollo genérico, y el lector debe seguirlo y adaptarlo, de acuerdo con el proceso de su empresa.

Este marco de pruebas contiene actividades que deben realizarse:

- Antes de que comience el desarrollo,
- Durante la definición y el diseño,
- Durante el desarrollo,
- Durante el despliegue y
- Durante el mantenimiento y las operaciones.

## Fase 1 antes de que comience el desarrollo

### Fase 1.1 Definir un SDLC

Antes de comenzar el desarrollo de la aplicación, se debe definir un SDLC adecuado donde la seguridad este implicita en cada etapa.

### Fase 1.2 Revisión de políticas y estándares

Asegúrese de que existan políticas, estándares y documentación adecuados. La documentación es muy importante ya que brinda a los equipos de desarrollo pautas y políticas que pueden seguir. Las personas solo pueden hacer lo correcto si saben qué es lo correcto.

Si la aplicación se va a desarrollar en Java, es fundamental que exista un estándar de codificación segura de Java. Si la aplicación va a utilizar criptografía, es fundamental que exista un estándar de criptografía. Ninguna política o norma puede cubrir todas las situaciones a las que se enfrentará el equipo de desarrollo. Al documentar los problemas comunes y predecibles, habrá menos decisiones que deban tomarse durante el proceso de desarrollo.

### Fase 1.3 Desarrollar criterios de medición y métricas y garantizar la trazabilidad

Antes de comenzar el desarrollo, planifique el programa de medición. Al definir los criterios que medirá, entrega visibilidad de los defectos en el proceso y en el producto. Es esencial definir las métricas antes de que comience el desarrollo, ya que puede ser necesario modificar el proceso para capturar los datos adecuados.

## Fase 2 Durante la definición y el diseño

### Fase 2.1 Revisión de los requisitos de seguridad

Los requisitos de seguridad definen cómo funciona una aplicación desde una perspectiva de seguridad. Es fundamental que se prueben los requisitos de seguridad. En este caso, probar significa probar las suposiciones que se hacen en los requisitos y probar para ver si hay brechas en las definiciones de los requisitos.

Por ejemplo, si existe un requisito de seguridad que establece que los usuarios deben estar registrados antes de que puedan acceder a la sección de documentos técnicos de un sitio web, ¿esto significa que el usuario debe estar registrado en el sistema o debe autenticarse? Asegúrese de que los requisitos no sean ambiguos.

Al buscar brechas en los requisitos, considere la búsqueda de mecanismos de seguridad como:

- Gestión de usuarios
- Autenticación
- Autorización
- Confidencialidad de los datos
- Integridad
- Responsabilidad (Accountability)
- Gestión de sesiones
- Seguridad del transporte
- Segregación del sistema por niveles
- Cumplimiento de normas y leyes (incluidas las normas de privacidad, gubernamentales y de la industria)

### Fase 2.2 Revisión de diseño y arquitectura

Las aplicaciones deben tener un diseño y una arquitectura documentados. Esta documentación puede incluir modelos, documentos textuales y otros artefactos similares. Es esencial probar estos artefactos para garantizar que el diseño y la arquitectura apliquen el nivel de seguridad adecuado según se define en los requisitos.

La identificación de fallas de seguridad en la fase de diseño, ademas de ser una etapa muy rentable para identificar fallas, también  puede ser uno de los lugares más efectivos para realizar cambios. Por ejemplo, si se identifica que el diseño requiere que las decisiones de autorización se tomen en varios lugares, puede ser apropiado considerar un componente de autorización central. Si la aplicación realiza la validación de datos en varios lugares, puede ser apropiado desarrollar un framework de validación central (es decir, fijar la validación de entrada en un solo lugar, en vez de hacerlo en varios lugares, es lejos mucho más económico)

Si se descubren debilidades, se las debe comunicar al arquitecto del sistema para enfoques alternativos.

### Fase 2.3 Crear y revisar modelos UML

Una vez que el diseño y la arquitectura estén completos, cree modelos en UML (Lenguaje de modelado unificado) que describan cómo funciona la aplicación. En algunos casos, es posible que ya estén disponibles. Utilice estos modelos para confirmar con los diseñadores de sistemas una comprensión exacta de cómo funciona la aplicación. Si se descubren debilidades, se las debe comunicar al arquitecto del sistema para enfoques alternativos.

### Fase 2.4 Crear y revisar modelos de amenazas

Si ya tiene las revisiones de diseño y arquitectura y los modelos UML que explican exactamente cómo funciona el sistema, realice un ejercicio de modelado de amenazas. Desarrolle escenarios de amenazas realistas. Analice el diseño y la arquitectura para asegurarse de que estas amenazas hayan sido mitigadas, aceptadas por la empresa o asignadas a un tercero, como una empresa de seguros. Cuando las amenazas identificadas no tienen estrategias de mitigación, revise el diseño y la arquitectura con el arquitecto de sistemas para modificar el diseño.

## Fase 3 Durante el desarrollo

En teoría, el desarrollo es la implementación de un diseño. Sin embargo, en el mundo real, muchas decisiones de diseño se toman durante el desarrollo del código. A menudo se trata de decisiones más pequeñas que tenían demasiado detalles para ser descritas en el diseño, o si suceden incidentes para los que no se ofreció ninguna política o guía estándar. Si el diseño y la arquitectura no fueran los adecuados, el desarrollador se enfrentará a muchas decisiones. Si las políticas y estándares son insuficientes, el desarrollador se enfrentará a incluso más decisiones.

### Fase 3.1 Recorrido del código (Code Walkthrough )

El equipo de seguridad debe realizar un recorrido de código con los desarrolladores y, en algunos casos, los arquitectos del sistema. Una revisión del tipo Walkthrough, es una mirada de alto nivel al código durante la cual los desarrolladores pueden explicar la lógica y el flujo del código implementado. Entrega al  equipo de revisión una comprensión general del código y permite a los desarrolladores explicar por qué ciertas cosas se desarrollaron de la forma en que se desarrollaron.

El propósito no es realizar una inspección formal del código, sino comprender a un alto nivel el flujo, el diseño y la estructura del código que conforma la aplicación.

### Fase 3.2 Revisiones de código (Code Review)

Teniendo una buena comprensión de cómo está estructurado el código y por qué ciertas cosas se codificaron de la forma en que estaban, el evaluador ahora puede examinar el código real en busca de defectos de seguridad.

Las revisiones estáticas, validan el código con un conjunto de listas de verificación, que incluyen:

- Requisitos comerciales de disponibilidad, confidencialidad e integridad;
- Checklists de guias de OWASP o del Top 10  para buscar riesgos de sobre-exposiciones técnicas (dependiendo de la profundidad de la revisión);
- Hallazgos específicos relacionados con el lenguaje o el framework utilizado, como por ejemplo el documento Scarlet para PHP o las [listas de verificación de codificación segura de Microsoft para ASP.NET](https://msdn.microsoft.com/en-us/library/ff648269.aspx) ; y
- Cualquier requisito específico de la industria, como Sarbanes-Oxley 404, COPPA, ISO/IEC 27002, APRA, HIPAA, pautas de Visa Merchant u otros regímenes regulatorios.

En cuanto al rendimiento de los recursos invertidos (principalmente tiempo), las revisiones de códigos estáticos producen rendimientos de calidad mucho más altos que cualquier otro método de revisión de seguridad y dependen menos de la habilidad del revisor. Sin embargo, no son una bala de plata (o solución milagrosa) y deben considerarse cuidadosamente dentro de un régimen de pruebas de espectro más amplio.

Para obtener más detalles sobre las listas de verificación de OWASP, consulte la última edición de [OWASP Top 10](https://owasp.org/www-project-top-ten/) .

## Fase 4 Durante la implementación

### Fase 4.1 Prueba de penetración de la aplicación

Después de haber probado los requisitos, analizado el diseño y realizado la revisión del código, se puede suponer que se han detectado todos los problemas. Es de esperar que este sea el caso, pero las pruebas de penetración de la aplicación después de que se haya implementado proporcionan una verificación adicional para garantizar que no se haya olvidado nada.

### Fase 4.2 Prueba de gestión de la configuración

La prueba de penetración de aplicaciones debe incluir un examen de cómo se implementó y aseguró la infraestructura. Es importante revisar los aspectos de la configuración, sin importar cuán pequeños sean, para asegurarse de que ninguno quede en una configuración predeterminada que pueda ser vulnerable a la explotación.

## Fase 5 Durante el mantenimiento y las operaciones

### Fase 5.1 Realización de revisiones de gestión operativa

Es necesario que exista un proceso que detalle cómo se administra el lado operativo tanto de la aplicación como de la infraestructura.

### Fase 5.2 Realizar comprobaciones periódicas de estado

Se deben realizar comprobaciones de estado mensuales o trimestrales tanto en la aplicación como en la infraestructura para garantizar que no se hayan introducido nuevos riesgos de seguridad y que el nivel de seguridad siga intacto.

### Fase 5.3 Asegurar la verificación de cambios

Después de que cada cambio se haya aprobado y verificado en el entorno de QA y se haya implementado en el entorno de producción, es vital que se verifique el cambio para garantizar que el nivel de seguridad no se haya visto afectado por el cambio. Esto debe integrarse en el proceso de gestión del cambio.

## Un flujo de trabajo típico de pruebas SDLC

La siguiente figura muestra un típico flujo de trabajo de pruebas para un SDLC.

![Flujo de trabajo de pruebas SDLC típico](images/Typical_SDLC_Testing_Workflow.gif)\
*Figure 3-1: Flujo de trabajo de pruebas SDLC típico*
