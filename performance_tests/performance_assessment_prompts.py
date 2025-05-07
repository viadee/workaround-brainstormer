PERFORMANCE_ASSESSMENT_PROMPTS = {
    "en": {
        "workaround_quality": """
            You are an expert process analyst with extensive experience investigating business processes across various industries.

            Consider the following process description: {process_description}

            Given the process description provided, please evaluate the following workarounds and determine which ones are relevant to the same domain. 

            **Workarounds:**
            {workaround_list}

            For each workaround, indicate true if it pertains to the specified domain, or false if it does not. 
            Additionally, provide a brief explanation for your reasoning.

            Return the assessment as a JSON object in the following format:
            {{
                "workarounds": [
                    {"assessment":[true/false],"explaination":[Explaination]},
                    ... (more assessments) ...
                ]
            }}
            """
         }
}