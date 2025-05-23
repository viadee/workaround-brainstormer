PROMPTS = {
    "en": {

        
"GenerateRolesPrompt" : """

You are an expert process analyst with extensive experience investigating business processes across various industries. Consider the process of the attached process diagram.
Let’s systematically analyze which roles respectively process participants/actors does the process description explicit and implicit include:
1.	First, list the explicid mentioned roles in the process description.
2.	Secondly, , consider the following questions and instructions to gather implicit mentioned or other relevant roles. Gather as much roles as you can: 	
-	what roles are most common or obvious in the described process domain e.g. industry the  process is performed in?
-	what roles perform the most critical tasks and what roles have desicion-making power or hold specific insides about the process?
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
-	type of employment (e.g. intern, full-time seasonal workers, etc.), 
-	function/department (e.g. Control tower, Accounting, Production line, Kitchen, )
Finally, from the basic population of roles, minimize the role selection by 
-	only including roles that can be differentiated by the nature of the role from the other roles, so that any of the final selected roles reflect a unique perspective on the process.
-	decide how many roles to select by weighing up if any role could give a valuable new perspective or if its nature is too similar to another role. 
-	do not include generic role names like “intern” or “Manager”, but “production manager” would be valid

Return as much roles as you can an JSON Array in the following format:
{{
 "roles" : [“Role1“, “Role2“]
}}
Minimize your answer length to only return the JSON Array and only two short sentences addressing the selection process.

""",


"GenerateMisfitsPrompt" : """

You are an expert process analyst with extensive experience investigating business processes across various industries. Consider the process of the attached process diagram and the following roles participating in the process:
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



Based on this analysis, for each given role, return three to seven Challenges as an JSON object in the following format:
-	Start each sentence with the role e.g. “As a consultant, ”
-	Continue with the context or action e.g. “As a consultant, when I am in a workshop with my client”
-	Finish with the identified challenge:  “As a consultant, when I am in a workshop with my client and can’t find the issue in the information system.”
{{
“role1”: [{{label: "short label of the challenge", text: "sentence"}}, {{label: "short label of the challenge", text: "sentence"}}, {{label: "short label of the challenge", text: "sentence"}}],
“role2”: [{{label: "short label of the challenge", text: "sentence"}}, {{label: "short label of the challenge", text: "sentence"}}]
}}, 

""",


"GenerateWorkaroundsPrompt": """


You are an expert process analyst with extensive experience investigating business processes across various industries. Consider the process of the attached process diagram and the following challenges that could occur in the process:
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
Finally, formulate a workaround that enables the role to overcome, bypass or minimize the challenge:
-	Present each workaround as a user story using the following format:
-	Template: "As a [role] [context], when [challenge], I [adaptive action] to [intended outcome]."
-	Provide 5 unique workarounds relevant to the process described.
Return the workarounds as a JSON object in the following format:
{{
"role1": [
{{
    "workaround":"As a [role] [context/activity], when [challenge], I [adaptive action] to [intended outcome].",
    "challengeLabel": "the label of the associated challenge"
}},
{{
    "workaround":"As a [role] [context/activity], when [challenge], I [adaptive action] to [intended outcome].",
    "Label": "the label of the associated challenge"
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
        "similar_no_image": """
            Sie sind ein erfahrener Prozessanalyst mit umfassender Erfahrung in der Untersuchung von Geschäftsprozessen in verschiedenen Branchen.

            Betrachten Sie den folgenden Prozess: {process_description}

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


