# Labeling strategy

As with many practices in operations, implementing a tagging strategy is a process of iteration and improvement. Start small with your immediate priority and grow the tagging schema as you need to.

Main focus of our tagging strategy is FinOps and Security, with that proposed strategy described with main focus on that two aspects.

## FinOps lens

Map spending data to the business
- Meaningful taxonomy of your costs
- Organizational breakdown (by division, business unit, management hierarchy)
- Functional Breakdown (by application)
- By cost center, project ID, or other identifier (map to available taxonomy)

Set tag strategy and compliance
- How to handle Untagged, Untaggable spending
- How to handle tag compliance

## Securiy lens

When breaches or other security problems happen, it’s important to classify the data and figure out how it affects security. Tagging opens the door to more secure operations.

- Application owner name
- Operations team / Team that is accountable for day-to-day operations
- Business criticality / Business impact of the resource or supported workload
- Disaster recovery / Business criticality of the application, workload, or service
- End date of the project / Date when the project is scheduled to be completed or when the application is scheduled for retirement (?)

# Proposed labels

| Use Case            | Label                                       | Rationale  | Exmaples |
|---------------------|-------------------------------------------|------------|-----------------------------------------------|
| Cost Allocation | name | The name of the application | AppA, AppB, AppC |
| Cost Allocation | version | The current version of the application (e.g., a SemVer 1.0, revision hash, etc.) | 5.7.21 |
| Cost Allocation | component | The component within the architecture	| frontend, backend, database |
| Cost Allocation | part-of | The name of a higher level application this one is part of | ProjectA, ProjectB, ProjectC |
| Automation | managed-by | The tool being used to manage the operation of an application | helm, argocd |
| OperationalExcellence | deployed-by | The controller/user who created this resource | hpotter, ggranger, rweasley |
| Security | business-criticality | Business criticality of the application, workload, or service | High, Medium, Low |

| Business criticality | Description                                                                                |
|----------------------|--------------------------------------------------------------------------------------------|
| High                 | Exploitation causes serious brand damage and financial loss with long-term business impact |
| Medium               | Applications connected to the internet that process financial or other private information |
| Low                  | Typically internal applications with non-critical business impact                          |
