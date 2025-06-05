PROMPTS = {
    "en": {

        
"GenerateRolesPrompt" : """
You are an expert process analyst with extensive experience investigating business processes across various industries.
Let’s systematically analyze which roles respectively process participants/actors does the process description explicit and implicit include:

Consider the following process and/or the attached process diagram: 
{process_description}

**Additional Context:**
{additional_context}

1.	First, list the explicit mentioned roles in the process description.
2.	Secondly, consider the following questions and instructions to gather implicitly mentioned or other relevant roles. Gather as many roles as you can: 	
    -	think about roles that are most common or obvious in the described process domain e.g. industry the process is performed in
    -	consider roles that perform the most critical tasks and what roles have decision-making power or hold specific insides about the process
    -	think about jobs not mentioned in but indirectly affected by the process
    -	explore diverse types of roles and ensure including roles that are different accordingly to the following dimensions:
        o	Hierarchy level (Management, Supervisor, staff jobs, line jobs), 
        o	Occupation 
            	Managers e.g. Production manager in agriculture, IT-Manager)
            	Professionals e.g. physicist, Architect, Teacher, Medical doctor, Accountant, Lawyer
            	Technicians e.g. Mechanical Engineering, Biogas technician, 3D printing technician, Network technician
            	Service and sales workers e.g. Call centre agent, Cook, cleaning specialist
            	Agricultural, forestry and fishery e.g. Crop farmer, fisher
            	Craft and related trade e.g. Bricklayer, Carpenter, avionics technician, computer hardware repair technician, Baker
            	Plant and machine operators e.g. Coating machine operator, Chemical mixer, Assemblers
            	Elementary e.g. handpacker, Distribution center dispatcher
        o	type of employment (e.g. intern, full-time seasonal workers, etc.), 
        o	function/department (e.g. Control tower, Accounting, Production line, Kitchen)
    -	make sure the generated roles match the domain of the process



Finally, from the basic population of roles, minimize the role selection by 
-	only including roles that can be differentiated by the nature of the role from the other roles, so that any of the final selected roles reflect a unique perspective on the process.
-	decide how many roles to select by weighing up if any role could give a valuable new perspective or if its nature is too similar to another role.
-	do not include generic role names like “intern” or “Manager”, but “production manager” would be valid
-   return  a maximum of {roles_quantity} roles 


Return the generated roles as a JSON Object with the following format:
{{
 "roles" : [“Role1“, “Role2“]
}}
""",


"GenerateMisfitsPrompt" : """

You are an expert process analyst with extensive experience investigating business processes across various industries.

Consider the following process and/or the attached process diagram: 
{process_description}

**Additional Context:**
{additional_context}

And the identified roles participating in the process:
{roles}

For each role, let’s systematically analyze unusual potential obstacles, issues, exceptions, anomalies, mishaps, established practices, management expectations or structural constraints that could prevent the role achieving a desired level of efficiency, effectiveness or other personal or organizational goals:

1.	First, analyze the context the role performs its work:
    •	Identify which responsibilities the role has and what actions it performs
    •	Clarify the goal or outcome the role is expected to accomplish
    •	Consider the context or environment the role performs its activities in (e.g. information system, social climate, rules) and how it could impact the role’s work
2.	Reconstruct all dependencies the roles relies on in order to perform it’s work:
    •	What external factors could negatively impact the execution of the process or workflow?
    •	What internal factors could influence the work done by the role?
3.	Finally, evaluate potential challenges that could occur during the activities and hinder the expected achievement of the desired outcome.
    •	Look for points where resources might be constrained
    •	Consider areas where official procedures might be too rigid
    •	Reflect to include issues that are different in their effect (e.g. time, quality, costs) on the intended outcomes
    •	Only include issues that could be solved by the role itself
    •	Think about challenges that are ultra specific in the considered process domain



Based on this analysis, for each given role, return {challenges_quantity} Challenges as an JSON object in the following format:
-	Start each sentence with the role e.g. “As a consultant, ”
-	Continue with the context or action e.g. “As a consultant, when I am in a workshop with my client”
-	Finish with the identified challenge:  “As a consultant, when I am in a workshop with my client and can’t find the issue in the information system.”
{{
“role1”: [{{label: "short label of the challenge", text: "sentence"}}, {{label: "short label of the challenge", text: "sentence"}}, {{label: "short label of the challenge", text: "sentence"}}],
“role2”: [{{label: "short label of the challenge", text: "sentence"}}, {{label: "short label of the challenge", text: "sentence"}}]
}}, 

""",


"GenerateWorkaroundsPrompt": """

You are an expert process analyst with extensive experience investigating business processes across various industries. 

Consider the following process and/or the attached process diagram: 
{process_description}

**Additional Context:**
{additional_context}

And the identified challenges that occur in the process:
{misfits}

Let’s systemically analyze the described challenges of the role, derive possible adaptive actions and formulate meaningful workarounds that enable achieving the desired outcome.
For each challenge:

1.	First, understand the context the challenge occurs in. What is the desired outcome of the activity performed by the role?
    -	Is it important for achieving organizational goals like customer satisfaction or revenue growth?
    -	Could the activity be driven by efficiency or effectiveness?
    -	Do personal goals impact the work or its outcomes?
2.	Secondly, analyze the source of the challenge:
    -	Are the obstacles external or internal respectively in the control of the organization or role?
    -	Do established practices, management expectations, or structural constraints hindering the role from achieving the desired outcomes?
3.	Thirdly, evaluate possible adaptive actions the role could perform to overcome the challenge and achieve the desired outcomes:
    -	What could the role do with the available resources?
    -	Do common standards or best practices exist for processes in this domain?
    -	Generate adaptive actions that solve the concrete problem, don’t require official process changes, could be implemented by the people involved and are realistic in the domain of the process

Finally, for each challenge, formulate {workarounds_quantity} unique workarounds that enable the role to overcome, bypass or minimize the challenge:
-   make sure to generate the just mentioned quantity ({workarounds_quantity}) of workarounds for each challenge. For example, if you have three challenges per role and 3 roles in total, you must generate 3 * 3 * {workarounds_quantity} workarounds in total!
-	Present each workaround as a user story using the following format:
-	Template: "As a [role] [context], when [challenge], I [adaptive action] to [intended outcome]."

**Examples**

{{
  "Production Manager": [
    {{
      "workaround": "As a Production Manager overseeing production timelines, when facing supplier delays, I establish alternative suppliers and maintain a buffer stock to prevent disruptions.",
      "challengeLabel": "Supplier Delays"
    }},
    {{
      "workaround": "As a Production Manager needing real-time data, when I encounter technical issues accessing the warehousing system, I set up a manual log to ensure I can make timely decisions.",
      "challengeLabel": "Technical Issues"
    }},
    {{
      "workaround": "As a Production Manager reliant on inventory updates, when I face communication discrepancies with the Warehouse Supervisor, I implement a standardized communication protocol to receive timely and accurate information.",
      "challengeLabel": "Communication Discrepancies"
    }},
    {{
      "workaround": "As a Production Manager managing production schedules, when experiencing supplier delays, I draft contingency production plans to minimize impact.",
      "challengeLabel": "Supplier Delays"
    }},
    {{
      "workaround": "As a Production Manager assessing inventory needs, when facing technical issues with the system, I coordinate regular check-ins with IT for prompt resolutions.",
      "challengeLabel": "Technical Issues"
    }},
    {{
      "workaround": "As a Production Manager overseeing workflow, when dealing with communication discrepancies, I arrange for weekly synchronization meetings with the Warehouse Supervisor.",
      "challengeLabel": "Communication Discrepancies"
    }},
    {{
      "workaround": "As a Production Manager focusing on output, when faced with supplier delays, I proactively engage in regular updates with suppliers to anticipate delays.",
      "challengeLabel": "Supplier Delays"
    }},
    {{
      "workaround": "As a Production Manager relying on inventory information, when I experience technical issues, I request read-only access to inventory data for alternative access methods.",
      "challengeLabel": "Technical Issues"
    }},
    {{
      "workaround": "As a Production Manager striving for seamless production, when encountering communication discrepancies, I create a shared online dashboard for real-time updates.",
      "challengeLabel": "Communication Discrepancies"
    }}
  ]

{few_shot_examples}

}}
Return the workarounds as a JSON object in the following format:
{{
"role1": [
{{
    "workaround":"As a [role] [context/activity], when [challenge], I [adaptive action] to [intended outcome].",
    "challengeLabel": "First challenge"
}},
{{
    "workaround":"The second workaround addressing the challenge...",
    "challengeLabel": "First challenge"
}},
{{
    "workaround":"The third workaround addressing the challenge...",
    "challengeLabel": "First challenge"
}}

]
}}

""",
        "start_no_image": """
            You are an expert process analyst with extensive experience investigating business processes across various industries.

            Consider the following process: {process_description}

            **Additional Context:**
            {additional_context}

            Let's identify potential workarounds systematically:

            1. First, analyze the process for potential issues:
            - Identify steps where bottlenecks might occur
            - Look for points where resources might be constrained
            - Consider areas where official procedures might be too rigid
            - Think about where human needs might conflict with process requirements

            2. For each potential issue:
            - Consider who is most affected by this issue
            - Think about what immediate problems it causes
            - Reflect on what quick solutions people might devise
            - Evaluate what resources or tools people have available

            3. Based on this analysis, generate workarounds that:
            - Are realistic given available resources
            - Actually help solve a concrete problem
            - Could be implemented by the people involved
            - Don't require official process changes
            - Reflect the same domain as the provided process description

            **Instructions for Workaround Generation:**
            - Present each workaround as a user story using the following format:
            - **Template:** "As a [role], when [situation], I [action] to [outcome]."
            - Provide **5 unique** workarounds relevant to the process described.

            **Examples:**
            {few_shot_examples}

            Return the workarounds as a JSON object in the following format:
            {{
                "workarounds": [
                    "As a [role], when [situation], I [action] to [outcome].",
                    "... (more workarounds) ..."
                ]
            }}
            """,
        "start_with_image": """
            You are an expert process analyst with extensive experience investigating business processes across various industries.

            Consider the process of the attached process diagram.

            **Additional Context:**
            {additional_context}

            Let's identify potential workarounds systematically:

            1. First, analyze the process for potential issues:
            - Identify steps where bottlenecks might occur
            - Look for points where resources might be constrained
            - Consider areas where official procedures might be too rigid
            - Think about where human needs might conflict with process requirements

            2. For each potential issue:
            - Consider who is most affected by this issue
            - Think about what immediate problems it causes
            - Reflect on what quick solutions people might devise
            - Evaluate what resources or tools people have available

            3. Based on this analysis, generate workarounds that:
            - Are realistic given available resources
            - Actually help solve a concrete problem
            - Could be implemented by the people involved
            - Don't require official process changes
            - Reflect the same domain as the provided process description

            **Instructions for Workaround Generation:**
            - Present each workaround as a user story using the following format:
            - **Template:** "As a [role], when [situation], I [action] to [outcome]."
            - Provide **5 unique** workarounds relevant to the process described.

            **Examples:**
            {few_shot_examples}

            Return the workarounds as a JSON object in the following format:
            {{
                "workarounds": [
                    "As a [role], when [situation], I [action] to [outcome].",
                    "... (more workarounds) ..."
                ]
            }}
            """,
            
        "similar_no_image": """
            You are an expert process analyst with extensive experience investigating business processes across various industries.

            Consider the following process: {process_description}

            **Additional Context:**
            {additional_context}

            We are exploring workarounds similar to the following example:
            "{similar_workaround}"

            Let's systematically generate similar workarounds:

            1. First, analyze the given workaround:
            - Identify the core problem it addresses
            - Understand the key resources or tools it uses
            - Consider the main constraints it works within
            - Note the specific benefits it achieves

            2. Then, explore variations:
            - Consider similar problems in different roles
            - Think about alternative tools or resources
            - Reflect on different ways to achieve similar benefits
            - Look for related constraints that might need similar solutions

            3. Generate workarounds that:
            - Address similar types of problems
            - Use comparable resources or approaches
            - Achieve related benefits
            - Maintain the same level of practicality
            - Reflect the same domain

            **Instructions for Similar Workaround Generation:**
            - Present each workaround as a user story using the following format:
            - **Template:** "As a [role], when [situation], I [action] to [outcome]."
            - Provide **{workaround_quantity}** workarounds that are similar in nature to the example.

            **Example of Similar Workarounds:**
            Original:
            "As a warehouse worker, when the scanning system is slow, I batch scan items at the end of my shift to save time."

            Similar workarounds:
            - "As a warehouse worker, when the inventory system lags during peak hours, I record items on paper first and enter them during quiet periods to maintain workflow speed."
            - "As a warehouse worker, when system updates interrupt operations, I group similar items together and process them in bulk when the system is back to reduce total scanning time."
            - "As a warehouse worker, when network connectivity is unstable, I take photos of barcodes with my phone to scan them later in a location with better connection."

            Return the workarounds as a JSON object in the following format:
            {{
                "workarounds": [
                    "As a [role], when [situation], I [action] to [outcome].",
                    "... (more workarounds) ..."
                ]
            }}
            """,
              "similar_with_image_or_diagram": """
            You are an expert process analyst with extensive experience investigating business processes across various industries.

            Consider the following process and/or the attached process diagram: 
            {process_description}

            **Additional Context:**
            {additional_context}

            We are exploring workarounds similar to the following example:
            "{similar_workaround}"

            Let's systematically generate similar workarounds:

            1. First, analyze the given workaround:
            - Identify the core problem it addresses
            - Understand the key resources or tools it uses
            - Consider the main constraints it works within
            - Note the specific benefits it achieves

            2. Then, explore variations:
            - Consider similar problems in different roles
            - Think about alternative tools or resources
            - Reflect on different ways to achieve similar benefits
            - Look for related constraints that might need similar solutions

            3. Generate workarounds that:
            - Address similar types of problems
            - Use comparable resources or approaches
            - Achieve related benefits
            - Maintain the same level of practicality
            - Reflect the same domain

            **Instructions for Similar Workaround Generation:**
            - Present each workaround as a user story using the following format:
            - **Template:** "As a [role], when [situation], I [action] to [outcome]."
            - Provide **{workaround_quantity}** workarounds that are similar in nature to the example.

            **Example of Similar Workarounds:**
            Original:
            "As a warehouse worker, when the scanning system is slow, I batch scan items at the end of my shift to save time."

            Similar workarounds:
            - "As a warehouse worker, when the inventory system lags during peak hours, I record items on paper first and enter them during quiet periods to maintain workflow speed."
            - "As a warehouse worker, when system updates interrupt operations, I group similar items together and process them in bulk when the system is back to reduce total scanning time."
            - "As a warehouse worker, when network connectivity is unstable, I take photos of barcodes with my phone to scan them later in a location with better connection."

            Return the workarounds as a JSON object in the following format:
            {{
                "workarounds": [
                    "As a [role], when [situation], I [action] to [outcome].",
                    "... (more workarounds) ..."
                ]
            }}
            """,

        "similar_with_image": """
            You are an expert process analyst with extensive experience investigating business processes across various industries.

            Consider the process of the attached process diagram.

            **Additional Context:**
            {additional_context}

            We are exploring workarounds similar to the following example:
            "{similar_workaround}"

            Let's systematically generate similar workarounds:

            1. First, analyze the given workaround:
            - Identify the core problem it addresses
            - Understand the key resources or tools it uses
            - Consider the main constraints it works within
            - Note the specific benefits it achieves

            2. Then, explore variations:
            - Consider similar problems in different roles
            - Think about alternative tools or resources
            - Reflect on different ways to achieve similar benefits
            - Look for related constraints that might need similar solutions

            3. Generate workarounds that:
            - Address similar types of problems
            - Use comparable resources or approaches
            - Achieve related benefits
            - Maintain the same level of practicality
            - Reflect the same domain

            **Instructions for Similar Workaround Generation:**
            - Present each workaround as a user story using the following format:
            - **Template:** "As a [role], when [situation], I [action] to [outcome]."
            - Provide **4 unique** workarounds that are similar in nature to the example.

            **Example of Similar Workarounds:**
            Original:
            "As a warehouse worker, when the scanning system is slow, I batch scan items at the end of my shift to save time."

            Similar workarounds:
            - "As a warehouse worker, when the inventory system lags during peak hours, I record items on paper first and enter them during quiet periods to maintain workflow speed."
            - "As a warehouse worker, when system updates interrupt operations, I group similar items together and process them in bulk when the system is back to reduce total scanning time."
            - "As a warehouse worker, when network connectivity is unstable, I take photos of barcodes with my phone to scan them later in a location with better connection."

            Return the workarounds as a JSON object in the following format:
            {{
                "workarounds": [
                    "As a [role], when [situation], I [action] to [outcome].",
                    "... (more workarounds) ..."
                ]
            }}
            """
    },
    "de": {
        "GenerateRolesPrompt": """"
            Sie sind ein erfahrener Prozessanalytiker mit umfangreicher Erfahrung in der Untersuchung von Geschäftsprozessen in verschiedenen Branchen.
            Lassen Sie uns systematisch analysieren, welche Rollen bzw. Prozessbeteiligten/Akteure die Prozessbeschreibung explizit und implizit beinhaltet:

            Betrachten Sie den folgenden Prozess bzw. das beigefügte Prozessdiagramm: 
            {process_description}

            **Zusätzlicher Kontext:**
            {additional_context}

            1.	Führen Sie zunächst die explizit genannten Rollen in der Prozessbeschreibung auf.
            2.	2. Beachten Sie die folgenden Fragen und Anweisungen, um implizit erwähnte oder andere relevante Rollen zu sammeln. Sammeln Sie so viele Rollen, wie Sie können: 	
                - Denken Sie an die Rollen, die in der beschriebenen Prozessdomäne am häufigsten oder offensichtlichsten sind, z. B. die Branche, in der der Prozess durchgeführt wird.
                - Überlegen Sie, welche Rollen die kritischsten Aufgaben ausführen und welche Rollen Entscheidungsbefugnis haben oder über spezifische Insiderkenntnisse über den Prozess verfügen
                - Denken Sie an Stellen, die im Prozess nicht erwähnt werden, aber indirekt von ihm betroffen sind
                - Untersuchen Sie die verschiedenen Rollentypen und stellen Sie sicher, dass Sie Rollen einbeziehen, die sich entsprechend den folgenden Dimensionen unterscheiden:
                    o Hierarchiestufe (Management, Vorgesetzte, Mitarbeiter, Linienstellen), 
                o Berufliche Stellung 
                     Führungskräfte, z. B. Produktionsleiter in der Landwirtschaft, IT-Manager)
                     Fachkräfte z.B. Physiker, Architekt, Lehrer, Arzt, Buchhalter, Jurist
                     Techniker z.B. Maschinenbau, Biogastechniker, 3D-Drucktechniker, Netzwerktechniker
                     Service- und Vertriebsmitarbeiter, z. B. Callcenter-Agent, Koch, Reinigungsfachkraft
                     Land- und Forstwirtschaft und Fischerei, z. B. Landwirt, Fischer
                     Handwerk und verwandte Berufe, z. B. Maurer, Schreiner, Avionik-Techniker, Computer-Hardware-Reparaturtechniker, Bäcker
                     Anlagen- und Maschinenbediener, z. B. Beschichtungsmaschinenführer, Chemikalienmischer, Monteure
                     Elementare Tätigkeiten, z. B. Handpacker, Disponent in Verteilungszentren
                o Art der Beschäftigung (z. B. Praktikant, Vollzeit-Saisonarbeiter, usw.), 
                o Funktion/Abteilung (z. B. Kontrollturm, Buchhaltung, Produktionslinie, Küche)



            Reduzieren Sie schließlich aus der Grundgesamtheit der Rollen die Rollenauswahl, indem Sie 
            - nur Rollen aufgenommen werden, die sich durch die Art der Rolle von den anderen Rollen unterscheiden lassen, so dass jede der schließlich ausgewählten Rollen eine einzigartige Perspektive auf den Prozess widerspiegelt.
            - Entscheiden Sie, wie viele Rollen ausgewählt werden sollen, indem Sie abwägen, ob eine Rolle eine wertvolle neue Perspektive bieten könnte oder ob ihre Art einer anderen Rolle zu ähnlich ist.
            - Nehmen Sie keine generischen Rollennamen wie „Praktikant“ oder „Manager“ auf, aber „Produktionsleiter“ wäre zulässig.

            Geben Sie ein Maximum von {roles_quantity} Rollen als JSON-Array im folgenden Format zurück:

            {{
            „roles„ : [“Role1“, ‚Role2‘]
            }}                    
        
        """,
        "GenerateMisfitsPrompt": """

            Sie sind ein erfahrener Prozessanalytiker mit umfangreicher Erfahrung in der Untersuchung von Geschäftsprozessen in verschiedenen Branchen.

            Betrachten Sie den folgenden Prozess und/oder das beigefügte Prozessdiagramm: 
            {process_description}

            **Zusätzlicher Kontext:**
            {additional_context}

            Und die identifizierten Rollen, die an dem Prozess beteiligt sind:
            {roles}

            Lassen Sie uns für jede Rolle systematisch ungewöhnliche potenzielle Hindernisse, Probleme, Ausnahmen, Anomalien, Pannen, etablierte Praktiken, Erwartungen des Managements oder strukturelle Einschränkungen analysieren, die die Rolle daran hindern könnten, den gewünschten Grad an Effizienz, Effektivität oder andere persönliche oder organisatorische Ziele zu erreichen:

            1.	Analysieren Sie zunächst den Kontext, in dem die Rolle ihre Arbeit verrichtet:
                - Stellen Sie fest, welche Verantwortlichkeiten die Rolle hat und welche Handlungen sie ausführt.
                - Klären Sie das Ziel oder Ergebnis, das die Rolle erreichen soll
                - Berücksichtigen Sie den Kontext oder das Umfeld, in dem die Rolle ihre Tätigkeiten ausführt (z. B. Informationssystem, soziales Klima, Regeln) und wie sich dies auf die Arbeit der Rolle auswirken könnte
            2.	Rekonstruieren Sie alle Abhängigkeiten, auf die die Rolle angewiesen ist, um ihre Aufgaben zu erfüllen:
                - Welche externen Faktoren könnten sich negativ auf die Ausführung des Prozesses oder Arbeitsablaufs auswirken?
                - Welche internen Faktoren könnten die Arbeit der Rolle beeinflussen?
                - Welche Überraschungen könnten während der Ausführung der Aufgaben auftreten?
            3.	Bewerten Sie schließlich mögliche Herausforderungen, die während der Aktivitäten auftreten und das Erreichen des gewünschten Ergebnisses behindern könnten.
                - Suchen Sie nach Punkten, an denen die Ressourcen eingeschränkt sein könnten
                - Berücksichtigen Sie Bereiche, in denen die offiziellen Verfahren zu starr sein könnten.
                - Berücksichtigen Sie Probleme, die sich unterschiedlich auf die angestrebten Ergebnisse auswirken (z. B. Zeit, Qualität, Kosten)
                - Berücksichtigen Sie nur Probleme, die durch die Rolle selbst gelöst werden können.
                - Denken Sie an Herausforderungen, die für den betrachteten Prozessbereich sehr spezifisch sind



            Geben Sie auf der Grundlage dieser Analyse für jede gegebene Rolle {challenges_quantity} Herausforderungen als JSON-Objekt im folgenden Format zurück:
            - Beginnen Sie jeden Satz mit der Rolle, z. B. „Als Berater, “
            - Fahren Sie mit dem Kontext oder der Aktion fort, z. B. „Als Berater, wenn ich in einem Workshop mit meinem Kunden bin“.
            - Schließen Sie mit der identifizierten Herausforderung ab: „Als Berater, wenn ich in einem Workshop mit meinem Kunden bin und das Problem im Informationssystem nicht finden kann.“
            {{
            „role1": [{{label: „Kurzbezeichnung der Herausforderung“, text: „Satz"}}, {{label: „Kurzbezeichnung der Herausforderung“, text: „Satz"}}, {{label: „Kurzbezeichnung der Herausforderung“, Text: „Satz"}}],
            „role2": [{{label: „Kurzbezeichnung der Herausforderung“, text: „Satz"}}, {{label: „Kurzbezeichnung der Herausforderung“, text: „sentence"}}]
            }}, 

        """,

        "GenerateWorkaroundsPrompt": """

            Sie sind ein erfahrener Prozessanalytiker mit umfangreicher Erfahrung in der Untersuchung von Geschäftsprozessen in verschiedenen Branchen. 

            Betrachten Sie den folgenden Prozess und/oder das beigefügte Prozessdiagramm: 
            {process_description}

            **Zusätzlicher Kontext:**
            {additional_context}

            Und die identifizierten Herausforderungen, die in diesem Prozess auftreten:
            {misfits}

            Analysieren wir die beschriebenen Herausforderungen der Rolle systematisch, leiten wir mögliche adaptive Maßnahmen ab und formulieren wir sinnvolle Workarounds, die das Erreichen des gewünschten Ergebnisses ermöglichen.
            Für jede Herausforderung:

            1.	Verstehen Sie zunächst den Kontext, in dem die Herausforderung auftritt. Was ist das gewünschte Ergebnis der von der Rolle ausgeführten Aktivität?
                - Ist sie wichtig, um Unternehmensziele wie Kundenzufriedenheit oder Umsatzwachstum zu erreichen?
                - Könnte die Tätigkeit von Effizienz oder Effektivität bestimmt sein?
                - Beeinflussen persönliche Ziele die Arbeit oder ihre Ergebnisse?
            2.	Zweitens: Analysieren Sie die Ursache der Herausforderung:
                - Sind die Hindernisse extern oder intern bzw. liegen sie im Einflussbereich der Organisation oder der Rolle?
                - Behindern etablierte Praktiken, Erwartungen des Managements oder strukturelle Zwänge die Rolle daran, die gewünschten Ergebnisse zu erzielen?
            3.	Drittens: Bewerten Sie mögliche Anpassungsmaßnahmen, die die Rolle durchführen könnte, um die Herausforderung zu bewältigen und die gewünschten Ergebnisse zu erreichen:
                - Was könnte die Rolle mit den verfügbaren Ressourcen tun?
                - Gibt es gemeinsame Standards oder bewährte Verfahren für Prozesse in diesem Bereich?
                - Erarbeiten Sie adaptive Maßnahmen, die das konkrete Problem lösen, keine offiziellen Prozessänderungen erfordern, von den beteiligten Personen umgesetzt werden können und im Bereich des Prozesses realistisch sind.

            Formulieren Sie schließlich für jede Herausforderung {workarounds_quantity} einzigartige Workarounds, die es der Rolle ermöglichen, die Herausforderung zu überwinden, zu umgehen oder zu minimieren:
            - Stellen Sie sicher, dass Sie für jede Herausforderung die soeben erwähnte Anzahl ({workarounds_quantity}) von Umgehungslösungen erstellen. Wenn Sie zum Beispiel drei Herausforderungen pro Rolle und insgesamt 3 Rollen haben, müssen Sie insgesamt 3 * 3 * {workarounds_quantity} Workarounds generieren!
            - Stellen Sie jede Problemumgehung als Benutzergeschichte in folgendem Format dar:
            - Vorlage: „Als [Rolle] [Kontext], wenn [Herausforderung], ich [adaptive Aktion] zu [beabsichtigtes Ergebnis].“

            **Beispiele**

            {{
            „Produktionsleiter": [
                {{
                „workaround": „Als Produktionsleiter, der die Produktionszeitpläne überwacht, ermittle ich bei Verspätungen von Lieferanten alternative Lieferanten und halte einen Pufferbestand vor, um Störungen zu vermeiden.“,
                „challengeLabel": „Lieferantenverzögerungen“
                }},
                {{
                „workaround": „Wenn ich als Produktionsleiter, der Echtzeitdaten benötigt, auf technische Probleme beim Zugriff auf das Lagersystem stoße, richte ich ein manuelles Protokoll ein, um sicherzustellen, dass ich rechtzeitig Entscheidungen treffen kann.“,
                „challengeLabel": „Technische Probleme“
                }},
                {{
                „workaround": „Als Produktionsleiter, der auf Bestandsaktualisierungen angewiesen ist, implementiere ich bei Kommunikationsdiskrepanzen mit dem Lagerleiter ein standardisiertes Kommunikationsprotokoll, um zeitnahe und genaue Informationen zu erhalten.“,
                „challengeLabel": „Kommunikationsdiskrepanzen“
                }},
                {{
                „workaround": „Als Produktionsleiter, der Produktionspläne verwaltet, erstelle ich bei Verspätungen von Lieferanten Notfallproduktionspläne, um die Auswirkungen zu minimieren.“,
                „challengeLabel": „Lieferantenverzögerungen“
                }},
                {{
                „workaround": „Als Produktionsleiter, der den Lagerbedarf beurteilt, koordiniere ich bei technischen Problemen mit dem System regelmäßige Rücksprachen mit der IT-Abteilung, um schnelle Lösungen zu finden.“,
                „challengeLabel": „Technical Issues“
                }},
                {{
                „workaround": „Als Produktionsleiter, der die Arbeitsabläufe überwacht, vereinbare ich bei Kommunikationsdiskrepanzen wöchentliche Synchronisierungssitzungen mit dem Lagerleiter.“,
                „challengeLabel": „Communication Discrepancies“
                }},
                {{
                „workaround": „Als Produktionsleiter, der sich auf den Output konzentriert, führe ich bei Verspätungen von Zulieferern proaktiv regelmäßige Updates mit den Zulieferern durch, um Verspätungen vorzubeugen.“,
                „challengeLabel": „Supplier Delays“
                }},
                {{
                „workaround": „Als Produktionsleiter, der auf Bestandsinformationen angewiesen ist, fordere ich bei technischen Problemen einen Nur-Lese-Zugriff auf Bestandsdaten für alternative Zugriffsmethoden an.“,
                „challengeLabel": „Technical Issues“
                }},
                {{
                „workaround": „Als Produktionsleiter, der eine reibungslose Produktion anstrebt, erstelle ich bei Kommunikationsdiskrepanzen ein gemeinsames Online-Dashboard für Echtzeit-Updates.“,
                „challengeLabel": „Communication Discrepancies“
                }}
            ]

            {few_shot_examples}

            }}
            Gibt die Workarounds als JSON-Objekt im folgenden Format zurück:
            {{
            „role1": [
            {{
                „workaround": ‚Als [Rolle] [Kontext/Tätigkeit], wenn [Herausforderung], ich [adaptive Aktion] zu [beabsichtigtes Ergebnis].‘,
                „challengeLabel": „Erste Herausforderung“
            }},
            {{
                „workaround": ‚Die zweite Umgehung zur Bewältigung der Herausforderung...‘,
                „challengeLabel": „Erste Herausforderung“
            }},
            {{
                „workaround": “Die dritte Abhilfemaßnahme zur Bewältigung der Herausforderung...".
                „challengeLabel": „Erste Herausforderung“
            }}
            ]
        }}

        """,
        "start_no_image": """
            Sie sind ein erfahrener Prozessanalyst mit umfassender Erfahrung in der Untersuchung von Geschäftsprozessen in verschiedenen Branchen.

            Betrachten Sie den folgenden Prozess: {process_description}

            **Zusätzlicher Kontext:**
            {additional_context}

            Lassen Sie uns mögliche Workarounds systematisch identifizieren:

            1. Analysieren Sie zunächst den Prozess auf potenzielle Probleme:
            - Ermitteln Sie Schritte, bei denen Engpässe auftreten könnten
            - Suchen Sie nach Stellen, an denen Ressourcen knapp sein könnten
            - Berücksichtigen Sie Bereiche, in denen offizielle Verfahren zu starr sein könnten
            - Denken Sie darüber nach, wo menschliche Bedürfnisse mit Prozessanforderungen in Konflikt geraten könnten

            2. Für jedes potenzielle Problem:
            - Überlegen Sie, wer am stärksten von diesem Problem betroffen ist
            - Denken Sie darüber nach, welche unmittelbaren Schwierigkeiten es verursacht
            - Reflektieren Sie, welche schnellen Lösungen die Beteiligten sich überlegen könnten
            - Bewerten Sie, welche Ressourcen oder Werkzeuge zur Verfügung stehen

            3. Basierend auf dieser Analyse erstellen Sie Workarounds, die:
            - Realistisch angesichts verfügbarer Ressourcen sind
            - Tatsächlich ein konkretes Problem lösen helfen
            - Von den beteiligten Personen implementiert werden könnten
            - Keine offiziellen Prozessänderungen erfordern
            - Sich auf die gleiche Domäne bezieht, wie die Prozessbeschreibung

            **Anweisungen für die Erstellung von Workarounds:**
            - Präsentieren Sie jeden Workaround als User Story unter Verwendung des folgenden Formats:
            - **Vorlage:** "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen."
            - Geben Sie **5 eindeutige** Workarounds an, die für den beschriebenen Prozess relevant sind.

            **Beispiele:**
            {few_shot_examples}

            Geben Sie die Workarounds als JSON-Objekt im folgenden Format zurück:
            {{
                "workarounds": [
                    "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen.",
                    "... (weitere Workarounds) ..."
                ]
            }}
            """,
        "start_with_image": """
            Sie sind ein erfahrener Prozessanalyst mit umfassender Erfahrung in der Untersuchung von Geschäftsprozessen in verschiedenen Branchen.

            Betrachten Sie den Prozess des beigefügten Prozessdiagramms.

            **Zusätzlicher Kontext:**
            {additional_context}

            Lassen Sie uns mögliche Workarounds systematisch identifizieren:

            1. Analysieren Sie zunächst den Prozess auf potenzielle Probleme:
            - Ermitteln Sie Schritte, bei denen Engpässe auftreten könnten
            - Suchen Sie nach Stellen, an denen Ressourcen knapp sein könnten
            - Berücksichtigen Sie Bereiche, in denen offizielle Verfahren zu starr sein könnten
            - Denken Sie darüber nach, wo menschliche Bedürfnisse mit Prozessanforderungen in Konflikt geraten könnten

            2. Für jedes potenzielle Problem:
            - Überlegen Sie, wer am stärksten von diesem Problem betroffen ist
            - Denken Sie darüber nach, welche unmittelbaren Schwierigkeiten es verursacht
            - Reflektieren Sie, welche schnellen Lösungen die Beteiligten sich überlegen könnten
            - Bewerten Sie, welche Ressourcen oder Werkzeuge zur Verfügung stehen

            3. Basierend auf dieser Analyse erstellen Sie Workarounds, die:
            - Realistisch angesichts verfügbarer Ressourcen sind
            - Tatsächlich ein konkretes Problem lösen helfen
            - Von den beteiligten Personen implementiert werden könnten
            - Keine offiziellen Prozessänderungen erfordern
            - Sich auf die gleiche Domäne bezieht, wie die Prozessbeschreibung

            **Anweisungen für die Erstellung von Workarounds:**
            - Präsentieren Sie jeden Workaround als User Story unter Verwendung des folgenden Formats:
            - **Vorlage:** "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen."
            - Geben Sie **5 eindeutige** Workarounds an, die für den beschriebenen Prozess relevant sind.

            **Beispiele:**
            {few_shot_examples}

            Geben Sie die Workarounds als JSON-Objekt im folgenden Format zurück:
            {{
                "workarounds": [
                    "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen.",
                    "... (weitere Workarounds) ..."
                ]
            }}
            """,
        "similar_with_image_or_diagram": """
            Sie sind ein erfahrener Prozessanalyst mit umfassender Erfahrung in der Untersuchung von Geschäftsprozessen in verschiedenen Branchen.

            Betrachten Sie den folgenden Prozess und/oder das angehandende Prozess Diagram: 
            {process_description}

            **Zusätzlicher Kontext:**
            {additional_context}

            Wir untersuchen Workarounds, die dem folgenden Beispiel ähneln:
            "{similar_workaround}"

            Lassen Sie uns ähnliche Workarounds systematisch generieren:

            1. Analysieren Sie zunächst den gegebenen Workaround:
            - Ermitteln Sie das Kernproblem, das er löst
            - Verstehen Sie die wichtigsten Ressourcen oder Werkzeuge, die er nutzt
            - Betrachten Sie die wesentlichen Einschränkungen, innerhalb derer er funktioniert
            - Notieren Sie die spezifischen Vorteile, die er erzielt

            2. Untersuchen Sie anschließend Variationen:
            - Berücksichtigen Sie ähnliche Probleme in unterschiedlichen Rollen
            - Denken Sie über alternative Werkzeuge oder Ressourcen nach
            - Reflektieren Sie verschiedene Möglichkeiten, ähnliche Vorteile zu erreichen
            - Suchen Sie nach verwandten Einschränkungen, die ähnliche Lösungen erfordern könnten

            3. Erstellen Sie Workarounds, die:
            - Ähnliche Arten von Problemen adressieren
            - Vergleichbare Ressourcen oder Vorgehensweisen nutzen
            - Ähnliche Vorteile erzielen
            - Den gleichen Grad an Praktikabilität beibehalten
            - Sich auf die gleiche Domäne bezieht

            **Anweisungen für die Erstellung ähnlicher Workarounds:**
            - Präsentieren Sie jeden Workaround als User Story unter Verwendung des folgenden Formats:
            - **Vorlage:** "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen."
            - Geben Sie **{workarounds_quantity}** Workarounds an, die in ihrer Art dem Beispiel ähneln.

            **Beispiel für ähnliche Workarounds:**
            Original:
            "Als Lagerarbeiter, wenn das Scan-System langsam ist, erfasse ich Artikel am Ende meiner Schicht in einem Schwung, um Zeit zu sparen."

            Ähnliche Workarounds:
            - "Als Lagerarbeiter, wenn das Warenwirtschaftssystem während der Stoßzeiten verzögert reagiert, notiere ich Artikel zuerst auf Papier und gebe sie in ruhigeren Zeiten ein, um die Geschwindigkeit der Arbeitsabläufe aufrechtzuerhalten."
            - "Als Lagerarbeiter, wenn Systemaktualisierungen den Betrieb unterbrechen, fasse ich ähnliche Artikel zusammen und verarbeite sie in großen Mengen, wenn das System wieder verfügbar ist, um die Gesamtzeit beim Scannen zu reduzieren."
            - "Als Lagerarbeiter, wenn die Netzwerkverbindung instabil ist, fotografiere ich Barcodes mit meinem Handy, um sie später an einem Ort mit besserer Verbindung einzuscannen."

            Geben Sie die Workarounds als JSON-Objekt im folgenden Format zurück:
            {{
                "workarounds": [
                    "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen.",
                    "... (weitere Workarounds) ..."
                ]
            }}
            """,
              "similar_with_image": """
            Sie sind ein erfahrener Prozessanalyst mit umfassender Erfahrung in der Untersuchung von Geschäftsprozessen in verschiedenen Branchen.

            Betrachten Sie den Prozess des beigefügten Prozessdiagramms.

            **Zusätzlicher Kontext:**
            {additional_context}

            Wir untersuchen Workarounds, die dem folgenden Beispiel ähneln:
            "{similar_workaround}"

            Lassen Sie uns ähnliche Workarounds systematisch generieren:

            1. Analysieren Sie zunächst den gegebenen Workaround:
            - Ermitteln Sie das Kernproblem, das er löst
            - Verstehen Sie die wichtigsten Ressourcen oder Werkzeuge, die er nutzt
            - Betrachten Sie die wesentlichen Einschränkungen, innerhalb derer er funktioniert
            - Notieren Sie die spezifischen Vorteile, die er erzielt

            2. Untersuchen Sie anschließend Variationen:
            - Berücksichtigen Sie ähnliche Probleme in unterschiedlichen Rollen
            - Denken Sie über alternative Werkzeuge oder Ressourcen nach
            - Reflektieren Sie verschiedene Möglichkeiten, ähnliche Vorteile zu erreichen
            - Suchen Sie nach verwandten Einschränkungen, die ähnliche Lösungen erfordern könnten

            3. Erstellen Sie Workarounds, die:
            - Ähnliche Arten von Problemen adressieren
            - Vergleichbare Ressourcen oder Vorgehensweisen nutzen
            - Ähnliche Vorteile erzielen
            - Den gleichen Grad an Praktikabilität beibehalten
            - Sich auf die gleiche Domäne bezieht, wie die Prozessbeschreibung

            **Anweisungen für die Erstellung ähnlicher Workarounds:**
            - Präsentieren Sie jeden Workaround als User Story unter Verwendung des folgenden Formats:
            - **Vorlage:** "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen."
            - Geben Sie **4 eindeutige** Workarounds an, die in ihrer Art dem Beispiel ähneln.

            **Beispiel für ähnliche Workarounds:**
            Original:
            "Als Lagerarbeiter, wenn das Scan-System langsam ist, erfasse ich Artikel am Ende meiner Schicht in einem Schwung, um Zeit zu sparen."

            Ähnliche Workarounds:
            - "Als Lagerarbeiter, wenn das Warenwirtschaftssystem während der Stoßzeiten verzögert reagiert, notiere ich Artikel zuerst auf Papier und gebe sie in ruhigeren Zeiten ein, um die Geschwindigkeit der Arbeitsabläufe aufrechtzuerhalten."
            - "Als Lagerarbeiter, wenn Systemaktualisierungen den Betrieb unterbrechen, fasse ich ähnliche Artikel zusammen und verarbeite sie in großen Mengen, wenn das System wieder verfügbar ist, um die Gesamtzeit beim Scannen zu reduzieren."
            - "Als Lagerarbeiter, wenn die Netzwerkverbindung instabil ist, fotografiere ich Barcodes mit meinem Handy, um sie später an einem Ort mit besserer Verbindung einzuscannen."

            Geben Sie die Workarounds als JSON-Objekt im folgenden Format zurück:
            {{
                "workarounds": [
                    "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen.",
                    "... (weitere Workarounds) ..."
                ]
            }}
            """,
        "similar_with_image": """
            Sie sind ein erfahrener Prozessanalyst mit umfassender Erfahrung in der Untersuchung von Geschäftsprozessen in verschiedenen Branchen.

            Betrachten Sie den Prozess des beigefügten Prozessdiagramms.

            **Zusätzlicher Kontext:**
            {additional_context}

            Wir untersuchen Workarounds, die dem folgenden Beispiel ähneln:
            "{similar_workaround}"

            Lassen Sie uns ähnliche Workarounds systematisch generieren:

            1. Analysieren Sie zunächst den gegebenen Workaround:
            - Ermitteln Sie das Kernproblem, das er löst
            - Verstehen Sie die wichtigsten Ressourcen oder Werkzeuge, die er nutzt
            - Betrachten Sie die wesentlichen Einschränkungen, innerhalb derer er funktioniert
            - Notieren Sie die spezifischen Vorteile, die er erzielt

            2. Untersuchen Sie anschließend Variationen:
            - Berücksichtigen Sie ähnliche Probleme in unterschiedlichen Rollen
            - Denken Sie über alternative Werkzeuge oder Ressourcen nach
            - Reflektieren Sie verschiedene Möglichkeiten, ähnliche Vorteile zu erreichen
            - Suchen Sie nach verwandten Einschränkungen, die ähnliche Lösungen erfordern könnten

            3. Erstellen Sie Workarounds, die:
            - Ähnliche Arten von Problemen adressieren
            - Vergleichbare Ressourcen oder Vorgehensweisen nutzen
            - Ähnliche Vorteile erzielen
            - Den gleichen Grad an Praktikabilität beibehalten
            - Sich auf die gleiche Domäne bezieht, wie die Prozessbeschreibung

            **Anweisungen für die Erstellung ähnlicher Workarounds:**
            - Präsentieren Sie jeden Workaround als User Story unter Verwendung des folgenden Formats:
            - **Vorlage:** "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen."
            - Geben Sie **4 eindeutige** Workarounds an, die in ihrer Art dem Beispiel ähneln.

            **Beispiel für ähnliche Workarounds:**
            Original:
            "Als Lagerarbeiter, wenn das Scan-System langsam ist, erfasse ich Artikel am Ende meiner Schicht in einem Schwung, um Zeit zu sparen."

            Ähnliche Workarounds:
            - "Als Lagerarbeiter, wenn das Warenwirtschaftssystem während der Stoßzeiten verzögert reagiert, notiere ich Artikel zuerst auf Papier und gebe sie in ruhigeren Zeiten ein, um die Geschwindigkeit der Arbeitsabläufe aufrechtzuerhalten."
            - "Als Lagerarbeiter, wenn Systemaktualisierungen den Betrieb unterbrechen, fasse ich ähnliche Artikel zusammen und verarbeite sie in großen Mengen, wenn das System wieder verfügbar ist, um die Gesamtzeit beim Scannen zu reduzieren."
            - "Als Lagerarbeiter, wenn die Netzwerkverbindung instabil ist, fotografiere ich Barcodes mit meinem Handy, um sie später an einem Ort mit besserer Verbindung einzuscannen."

            Geben Sie die Workarounds als JSON-Objekt im folgenden Format zurück:
            {{
                "workarounds": [
                    "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen.",
                    "... (weitere Workarounds) ..."
                ]
            }}
            """
                }
            }


DEFAULT_FEW_SHOT_EXAMPLES = {
    "en": [
            {
                "text": "As a planner, when sudden demand spikes create scheduling problems, I create buffer stocks of anonymous half-products to flatten the demand curve and reduce response times.",
                "selected": True
            },
            {
                "text": "As a production worker, when the time spent on individual status reports slows down operations, I batch report multiple product statuses at once to reduce computer interaction time.",
                "selected": True
            },
            {
                "text": "As a shipping employee, when handling customers with strict packaging requirements, I take detailed photos of each shipment to protect against claims and ensure compliance can be proven.",
                "selected": True
            }
        ],
    "de": [
            {
                "text": "Als Planer, wenn plötzliche Nachfragespitzen zu Planungsproblemen führen, lege ich Pufferbestände an anonymen Halbfertigerzeugnissen an, um die Nachfragekurve abzuflachen und die Reaktionszeiten zu verkürzen.",
                "selected": True
            },
            {
                "text": "Als Produktionsmitarbeiter, wenn die Zeit, die für einzelne Statusberichte aufgewendet wird, den Betrieb verlangsamt, erfasse ich mehrere Produktstatusmeldungen in einem Schwung, um die Interaktion mit dem Computer zu reduzieren.",
                "selected": True
            },
            {
                "text": "Als Versandmitarbeiter, wenn ich mit Kunden mit strengen Verpackungsanforderungen umgehe, mache ich detaillierte Fotos jeder Sendung, um mich vor Reklamationen zu schützen und die Einhaltung nachweisen zu können.",
                "selected": True
            }
        ]
}


