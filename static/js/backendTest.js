class BackendTest{

    returnRoles = () => {
        return {
            roles:["Production Supervisor","Warehouse Manager","Logistics Coordinator"]
        }
    }

    returnMisfits = () => {
        return {
            "Production Supervisor": [
                {"label": "Workforce Management Issues", "text": "As a Production Supervisor, when I am managing my team and face unexpected absenteeism, it disrupts the production schedule."},
                {"label": "Equipment Downtime", "text": "As a Production Supervisor, when I am overseeing production and machinery breaks down, it halts operations and impacts delivery timelines."},
                {"label": "Quality Compromise", "text": "As a Production Supervisor, when I am trying to meet production targets and receive substandard materials, it jeopardizes the overall quality of the products."}
            ],
            "Warehouse Manager": [
                {"label": "Inventory Discrepancies", "text": "As a Warehouse Manager, when I am reconciling inventory and find discrepancies between physical stock and system records, it complicates order fulfillment."},
                {"label": "Space Constraints", "text": "As a Warehouse Manager, when I am organizing space and face overstock situations, it restricts my ability to efficiently manage inventory."},
                {"label": "Logistics Delays", "text": "As a Warehouse Manager, when I am coordinating with logistics and experience delays in transportation, it causes a backlog in shipments."}
            ],
            "Logistics Coordinator": [
                {"label": "Unexpected Shipping Costs", "text": "As a Logistics Coordinator, when I am planning shipments and incur unexpected tariffs, it increases operational costs."},
                {"label": "Weather Disruptions", "text": "As a Logistics Coordinator, when I am scheduling deliveries and face weather-related delays, it impacts delivery windows."},
                {"label": "Vendor Reliability Issues", "text": "As a Logistics Coordinator, when I rely on third-party carriers that do not adhere to schedules, it disrupts the overall logistics flow."}
            ],
        }
    }

    returnWorkarounds = () => {
        return {
            "Production Supervisor": [
                {
                    "misfitLabel": "Workforce Management Issues",
                    "workaround": "As a customer waiting for my pizza, when the delivery exceeds 30 minutes and I feel frustration, I proactively call the delivery service to get updates and attempt to expedite the process to reduce my waiting time and dissatisfaction."
                },
                {
                    "misfitLabel": "Equipment Downtime",
                    "workaround": "As a customer needing to complain, when complaint channels are unclear or unresponsive, I utilize any available direct contact options such as social media or review platforms to voice issues and seek quicker resolution."
                },
                {
                    "misfitLabel": "Quality Compromise",
                    "workaround": "As a customer considering canceling after a complaint, when unsure about timing constraints, I immediately confirm cancellation policies via phone or support chat to ensure my cancellation occurs within allowed time frames and avoid missing the window."
                }
            ],
            "Warehouse Manager": [
                {
                    "misfitLabel": "Inventory Discrepancies",
                    "workaround": "As a delivery manager coordinating kitchen and delivery, when I face difficulty synchronizing processes, I establish informal real-time communication channels like instant messaging groups to quickly update on order statuses and reduce delays or mistakes."
                },
                {
                    "misfitLabel": "Space Constraints",
                    "workaround": "As a delivery manager handling escalated complaints, when internal communication is slow, I empower delivery agents with authority and information to resolve common issues on the spot, accelerating resolutions and improving customer satisfaction."
                },
                {
                    "misfitLabel": "Logistics Delays",
                    "workaround": "As a delivery manager balancing efficiency and satisfaction, when strict time policies risk harming satisfaction, I allow flexible delivery time windows with customer notifications explaining delays, managing expectations while maintaining operational flow."
                }
            ],
            "Logistics Coordinator": [
                {
                    "misfitLabel": "Unexpected Shipping Costs",
                    "workaround": "As a delivery agent receiving complaints, when communication with kitchen/logistics is slow, I independently track order progress through system tools or directly call the kitchen to get timely updates, enabling quicker, accurate responses to customers."
                },
                {
                    "misfitLabel": "Weather Disruptions",
                    "workaround": "As a delivery agent under delivery time pressure, when stress risks poor service, I prioritize safe and quality delivery over rushing, while communicating realistic arrival estimates to customers to prevent dissatisfaction from unmet expectations."
                },
                {
                    "misfitLabel": "Vendor Reliability Issues",
                    "workaround": "As a delivery agent managing cancellations post-complaint, when rigid processes delay cancellations, I document and escalate urgent cancellation requests to management for exception handling, ensuring customer needs are respected without breaching policies."
                }
            ]
        }
    }

}

export default BackendTest;