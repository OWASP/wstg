# Prologo de Eoin Keary

El Problema del software inseguro es quizás el problema técnico más importante desafío de nuestro tiempo. El dramático aumento de las aplicaciones web que permiten negocios, redes, etc. solo ha agravado los requísitos para establecer un enfoque sólido para escribir y proteger nuestra internet, aplicaciones web y datos.

En el Proyecto de Seguridad de Aplicaciones Web Abiertas® (OWASP®), intentamos hacer del mundo un lugar donde el software inseguro sea la anomalía, no la norma. La guía de pruebas de OWASP tiene un importante papel en la resolución de este grave problema. Es de vital importancia que nuestro enfoque para probar el software para los problemas de seguridad se base en los principios de la ingeniería y la ciencia. Necesitamos un enfoque consistente, repetible y definido para probar aplicaciones web. Un mundo sin algunos estándares mínimos en términos de ingeniería y tecnología es un mundo en caos.

No hace falta decir que no se puede construir una aplicación segura sin realizar pruebas de seguridad en ella. Las pruebas son parte de un enfoque más amplio para construir un sistema seguro. Muchas organizaciones de desarrollo de software no incluyen las pruebas de seguridad como parte de su proceso estándar de desarrollo de software. Lo que es aún peor es que muchos proveedores de seguridad entregan pruebas con diversos grados de calidad y rigor.

Las pruebas de seguridad, por sí mismas, no son una medida independiente particularmente buena de cuán segura es una aplicación, porque hay un número infinito de maneras en que un atacante podría ser capaz de hacer que una aplicación se rompa, y simplemente no es posible probarlas todas. No podemos hackearnos a nosotros mismos de forma segura ya que sólo tenemos un tiempo limitado para probar y defendernos cuando un atacante no tiene tales restricciones.

En conjunto con otros proyectos de OWASP como la Guía de Revisión de Código, la Guía de Desarrollo y herramientas como [OWASP ZAP](https://www.zaproxy.org/), este es un gran comienzo hacia la construcción y mantenimiento de aplicaciones seguras. Esta Guía de Pruebas le mostrará cómo verificar la seguridad de su aplicación en ejecución. Recomiendo encarecidamente el uso de estas guías como parte de sus iniciativas de seguridad de aplicaciones.

## ¿Porqué OWASP?

Crear una guía como esta es una enorme tarea, requiere la experiencia de cientos de personas de todo el mundo. Hay muchas formas de probar las fallas de seguridad y esta guía captura el consenso de los lideres expertos en cómo realizar estas pruebas de forma rápida, precisa y eficiente. OWASP brinda a personas con afines de seguridad la capacidad de trabajar juntos y establecer un enfoque de practica líder para un problema de seguridad.

La importancia de tener esta guía disponible de forma completamente gratuita y abierta es importante para la misión de la fundación. Le da a cualquiera la capacidad de entender las técnicas utilizadas para probar los problemas de seguridad comunes. La seguridad no debería ser un arte negro o un secreto cerrado que sólo unos pocos pueden practicar. Debería estar abierta a todos y no ser exclusiva de los profesionales de la seguridad, sino también de los desarrolladores, QA y directores técnicos. El proyecto para construir esta guía mantiene esta experiencia en las manos de las personas que la necesitan - tú, yo y cualquiera que esté involucrado en la construcción de software.

Esta guía debe llegar a las manos de los desarrolladores y probadores de software. No hay suficientes expertos en seguridad de aplicaciones en el mundo para hacer una reducción significativa en el problema general. La responsabilidad inicial de la seguridad de las aplicaciones debe recaer en los hombros de los desarrolladores porque ellos escriben el código. No debería ser una sorpresa que los desarrolladores no estén produciendo código seguro si no lo están probando o considerando los tipos de errores que introducen vulnerabilidad.

Mantener esta información actualizada es un aspecto crítico de este proyecto de guía. Al adoptar el enfoque del wiki, la comunidad OWASP puede evolucionar y ampliar la información de esta guía para mantenerse al día con el rápido movimiento del panorama de las amenazas a la seguridad de las aplicaciones.

Esta guía es un gran testimonio de la pasión y energía que nuestros miembros y voluntarios del proyecto tienen por este tema. Ciertamente ayudará a cambiar el mundo una línea de código a la vez.

## Adaptación y Preparación

Debe de adoptar esta guía en su organización. Puede que necesite adoptar la información para que coincida con las tecnologías, procesos y estructuración.

En general hay varios roles diferentes dentro de las organizaciones que pueden utilizar esta guía:

- Los desarrolladores deben utilizar esta guía para asegurarse de que están produciendo un código seguro. Estas pruebas deben formar parte de los procedimientos normales de prueba de códigos y unidades.
- Los probadores/testeadores de software y el control de calidad (QA) deben utilizar esta guía para ampliar el conjunto de pruebas en casos donde aplique a la aplicación. Detectar estas vulnerabilidades temprano ahorra tiempo y esfuerzo considerablemente mas adelante.
- Los especialistas en seguridad deben utilizar esta guía en combinación con otras técnicas como una forma de verificar que no se hayan pasado por alto agujeros de seguridad en una aplicación.
- Los jefes de proyectos deben considerar la razón por la que existe esta guía y que los problemas de seguridad se manifiestan a través de errores en el código y el diseño.

Lo más importante que hay que recordar cuando se realizan pruebas de seguridad es volver a establecer continuamente las prioridades. Hay un número infinito de formas posibles en que una aplicación podría fallar, y las organizaciones siempre tienen tiempo y recursos de prueba limitados. Asegúrese de que el tiempo y los recursos se gasten de forma inteligente. Trate de centrarse en los agujeros de seguridad que son un riesgo real para su negocio. Trate de contextualizar el riesgo en términos de la aplicación y sus casos de uso.

La mejor manera de ver esta guía es como un conjunto de técnicas que puedes usar para encontrar diferentes tipos de agujeros de seguridad. Pero no todas las técnicas son igualmente importantes. Trate de evitar utilizar la guía como una lista de comprobación, las nuevas vulnerabilidades siempre se manifiestan y ninguna guía puede ser una lista exhaustiva de "cosas para probar", sino más bien un gran lugar para empezar.

## Los roles de las herramientas automatizadas

Hay varias empresas que venden herramientas de análisis y pruebas de seguridad automatizadas. Recuerde las limitaciones de estas herramientas para que pueda usarlas para lo que son buenas. Como dijo Michael Howard en la Conferencia AppSec de la OWASP en Seattle en 2006, "¡Las herramientas no hacen que el software sea seguro! Ayudan a escalar el proceso y ayudan a hacer cumplir la política".

Lo más importante es que estas herramientas son genéricas, es decir, no están diseñadas para su código personalizado, sino para aplicaciones en general. Esto significa que aunque pueden encontrar algunos problemas genéricos, no tienen el suficiente conocimiento de su aplicación como para permitirles detectar la mayoría de los fallos. En mi experiencia, los problemas de seguridad más graves son los que no son genéricos, sino que están profundamente entrelazados en la lógica de su negocio y en el diseño de su aplicación personalizada.

Estas herramientas también pueden ser muy útiles, ya que encuentran muchos problemas potenciales. Aunque ejecutar las herramientas no lleva mucho tiempo, cada uno de los problemas potenciales toma tiempo para investigar y verificar. Si el objetivo es encontrar y eliminar los fallos más graves lo más rápido posible, considere si su tiempo se emplea mejor con herramientas automatizadas o con las técnicas descritas en esta guía. Aún así, estas herramientas son ciertamente parte de un programa de seguridad de aplicaciones bien equilibrado. Utilizadas de manera inteligente, pueden apoyar sus procesos generales para producir un código más seguro.

## Llamada a la acción

Si está construyendo, diseñando o probando software, le recomiendo encarecidamente que se familiarice con la guía de pruebas de seguridad de este documento. Es una gran hoja de ruta (o road map) para probar los problemas más comunes a los que se enfrentan las aplicaciones hoy en día, pero no es exhaustiva. Si encuentra errores, por favor, añada una nota a la página de discusión o haga el cambio usted mismo. Estarás ayudando a miles de personas que utilizan esta guía.

Por favor considere [unirse a nosotros](https://owasp.org/membership/) como miembro  individual o corporativo para que podamos seguir produciendo materiales como esta guía de pruebas/testeo y todos los demás grandes proyectos en OWASP.

Gracias a todos los colaboradores pasados y futuros de esta guía, su trabajo ayudará a que las aplicaciones en todo el mundo sean más seguras.

--Eoin Keary, Miembro de la Junta de la OWASP, Abril 19, 2013

Open Web Application Security Project y OWASP son marcas registradas de la Fundación OWASP, Inc.
