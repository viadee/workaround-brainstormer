PROMPTS = {
    "en": {
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

            **Instructions for Workaround Generation:**
            - Present each workaround as a user story using the following format:
            - **Template:** "As a [role], when [situation], I [action] to [outcome]."
            - Provide **5 unique** workarounds relevant to the process described.

            **Examples:**
            - "As a planner, when sudden demand spikes create scheduling problems, I create buffer stocks of anonymous half-products to flatten the demand curve and reduce response times."
            - "As a production worker, when the time spent on individual status reports slows down operations, I batch report multiple product statuses at once to reduce computer interaction time."
            - "As a shipping employee, when handling customers with strict packaging requirements, I take detailed photos of each shipment to protect against claims and ensure compliance can be proven."

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

            **Instructions for Workaround Generation:**
            - Present each workaround as a user story using the following format:
            - **Template:** "As a [role], when [situation], I [action] to [outcome]."
            - Provide **5 unique** workarounds relevant to the process described.

            **Examples:**
            - "As a planner, when sudden demand spikes create scheduling problems, I create buffer stocks of anonymous half-products to flatten the demand curve and reduce response times."
            - "As a production worker, when the time spent on individual status reports slows down operations, I batch report multiple product statuses at once to reduce computer interaction time."
            - "As a shipping employee, when handling customers with strict packaging requirements, I take detailed photos of each shipment to protect against claims and ensure compliance can be proven."

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

            **Anweisungen für die Erstellung von Workarounds:**
            - Präsentieren Sie jeden Workaround als User Story unter Verwendung des folgenden Formats:
            - **Vorlage:** "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen."
            - Geben Sie **5 eindeutige** Workarounds an, die für den beschriebenen Prozess relevant sind.

            **Beispiele:**
            - "Als Planer, wenn plötzliche Nachfragespitzen zu Planungsproblemen führen, lege ich Pufferbestände an anonymen Halbfertigerzeugnissen an, um die Nachfragekurve abzuflachen und die Reaktionszeiten zu verkürzen."
            - "Als Produktionsmitarbeiter, wenn die Zeit für einzelne Statusberichte den Betrieb verlangsamt, erfasse ich mehrere Produktstatusmeldungen in einem Schwung, um die Interaktion mit dem Computer zu reduzieren."
            - "Als Versandmitarbeiter, wenn ich mit Kunden mit strengen Verpackungsanforderungen zu tun habe, mache ich detaillierte Fotos von jeder Sendung, um mich vor Reklamationen zu schützen und die Einhaltung nachweisen zu können."

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

            **Anweisungen für die Erstellung von Workarounds:**
            - Präsentieren Sie jeden Workaround als User Story unter Verwendung des folgenden Formats:
            - **Vorlage:** "Als [Rolle], wenn [Situation], handle ich [Aktion], um [Ergebnis] zu erreichen."
            - Geben Sie **5 eindeutige** Workarounds an, die für den beschriebenen Prozess relevant sind.

            **Beispiele:**
            - "Als Planer, wenn plötzliche Nachfragespitzen zu Planungsproblemen führen, lege ich Pufferbestände an anonymen Halbfertigerzeugnissen an, um die Nachfragekurve abzuflachen und die Reaktionszeiten zu verkürzen."
            - "Als Produktionsmitarbeiter, wenn die Zeit für einzelne Statusberichte den Betrieb verlangsamt, erfasse ich mehrere Produktstatusmeldungen in einem Schwung, um die Interaktion mit dem Computer zu reduzieren."
            - "Als Versandmitarbeiter, wenn ich mit Kunden mit strengen Verpackungsanforderungen zu tun habe, mache ich detaillierte Fotos von jeder Sendung, um mich vor Reklamationen zu schützen und die Einhaltung nachweisen zu können."

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
