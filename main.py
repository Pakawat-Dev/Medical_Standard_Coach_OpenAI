"""
ZenTH ISO Standards Coach - Medical Device Compliance Assistant.

This module implements a multi-agent system for providing expert guidance
on medical device standards compliance (ISO 13485, IEC 62304, IEC 82304-1,
ISO 14971).

"""

import os
import asyncio
from typing import Final, Optional
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import (
    MaxMessageTermination,
    TextMentionTermination
)
from autogen_agentchat.teams import RoundRobinGroupChat


# Load environment variables
load_dotenv()

# Constants
MODEL_NAME: Final[str] = "gpt-5-mini-2025-08-07"
MAX_INNER_MESSAGES: Final[int] = 6
MAX_OUTER_TURNS: Final[int] = 2
APPROVAL_KEYWORD: Final[str] = "APPROVE"
SEPARATOR: Final[str] = "=" * 80
EXIT_COMMANDS: Final[tuple] = ("quit", "exit", "q", "bye")

# System Messages (cached as constants for better performance)
ZENTH_COACH_SYSTEM_MESSAGE: Final[str] = """
You are ZenTH ISO Standards Coach, a specialized Technical Auditor Agent \
for medical device standards.

## Your Core Expertise:
- **ISO 13485:2016**: Quality Management Systems for medical devices
- **IEC 62304:2006+A1:2015**: Medical device software lifecycle processes
- **IEC 82304-1:2016**: Health software standards
- **ISO 14971:2019**: Risk management for medical devices

## Your Responsibilities:
1. Provide expert guidance on compliance with medical device regulations
2. Assess documentation completeness and accuracy
3. Review risk management processes and traceability
4. Explain software safety classification (Class A, B, C)
5. Guide on quality management system implementation
6. Offer gap analysis and audit methodology advice

## Your Capabilities:
- Evaluate technical documentation and design controls
- Assess software architecture and validation evidence
- Provide guidance on SOUP (Software of Unknown Provenance) management
- Explain hazard identification techniques (FMEA, FTA, HAZOP)
- Guide on benefit-risk analysis and post-market surveillance
- Advise on global regulatory requirements (FDA, EU MDR, Health Canada)

## CRITICAL MEDICAL GUARDRAILS:
⚠️ Never provide diagnosis/treatment or device operation guidance.
If asked for clinical advice, respond:
"I'm not a medical professional and can't provide clinical guidance. 
Please consult a qualified clinician or your organization's approved \
procedures."
Then offer relevant policy/training materials.

## Your Approach:
- Provide clear, actionable findings with specific standard clause \
references
- Balance technical thoroughness with practical business considerations
- Maintain objectivity and professional integrity
- Stay current with regulatory changes and state-of-the-art considerations

Respond professionally, technically accurate, and always prioritize \
patient safety.
"""

COMPLIANCE_REVIEWER_SYSTEM_MESSAGE: Final[str] = """
You are a Compliance Reviewer specializing in medical device regulations.

Your role:
1. Review ZenTH Coach's guidance for regulatory accuracy
2. Identify any missing regulatory considerations
3. Ensure alignment with FDA, EU MDR, and international standards
4. Flag potential compliance gaps or risks
5. Validate that all standard clauses are properly referenced

Provide critical feedback and validation. If the guidance is complete and \
accurate, respond with 'APPROVE'.
If improvements needed, specify exactly what's missing or incorrect.
"""

DOCUMENTATION_FORMATTER_SYSTEM_MESSAGE: Final[str] = """
You are a Documentation Formatter for medical device technical documentation.

Your role:
1. Format the guidance into clear, professional documentation
2. Structure information with proper headings and sections
3. Ensure traceability to relevant standard clauses
4. Add references and citations where appropriate
5. Make the content audit-ready and regulatory-compliant

Present the final output in a clear, professional format suitable for QMS \
documentation.
"""


def create_model_client() -> OpenAIChatCompletionClient:
    """
    Create and configure the OpenAI model client.

    Returns:
        OpenAIChatCompletionClient: Configured model client instance.

    Raises:
        EnvironmentError: If OPENAI_API_KEY is not set.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable not set. "
            "Please set it before running the application."
        )

    return OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=api_key,
    )


def create_zenth_coach_agent(
    model_client: OpenAIChatCompletionClient
) -> AssistantAgent:
    """
    Create the ZenTH ISO Standards Coach agent.

    Args:
        model_client: OpenAI model client instance.

    Returns:
        AssistantAgent: Configured ZenTH coach agent.
    """
    return AssistantAgent(
        name="ZenTH_ISO_Standards_Coach",
        model_client=model_client,
        system_message=ZENTH_COACH_SYSTEM_MESSAGE,
    )


def create_compliance_reviewer_agent(
    model_client: OpenAIChatCompletionClient
) -> AssistantAgent:
    """
    Create the Compliance Reviewer agent.

    Args:
        model_client: OpenAI model client instance.

    Returns:
        AssistantAgent: Configured compliance reviewer agent.
    """
    return AssistantAgent(
        name="Compliance_Reviewer",
        model_client=model_client,
        system_message=COMPLIANCE_REVIEWER_SYSTEM_MESSAGE,
    )


def create_documentation_formatter_agent(
    model_client: OpenAIChatCompletionClient
) -> AssistantAgent:
    """
    Create the Documentation Formatter agent.

    Args:
        model_client: OpenAI model client instance.

    Returns:
        AssistantAgent: Configured documentation formatter agent.
    """
    return AssistantAgent(
        name="Documentation_Formatter",
        model_client=model_client,
        system_message=DOCUMENTATION_FORMATTER_SYSTEM_MESSAGE,
    )


def create_standards_team(
    zenth_coach: AssistantAgent,
    compliance_reviewer: AssistantAgent
) -> RoundRobinGroupChat:
    """
    Create the inner standards team with termination conditions.

    Args:
        zenth_coach: ZenTH ISO Standards Coach agent.
        compliance_reviewer: Compliance Reviewer agent.

    Returns:
        RoundRobinGroupChat: Configured standards team.
    """
    termination = (
        TextMentionTermination(APPROVAL_KEYWORD) |
        MaxMessageTermination(max_messages=MAX_INNER_MESSAGES)
    )

    return RoundRobinGroupChat(
        participants=[zenth_coach, compliance_reviewer],
        termination_condition=termination,
    )


def create_final_team(
    society_of_mind: SocietyOfMindAgent,
    documentation_formatter: AssistantAgent
) -> RoundRobinGroupChat:
    """
    Create the final team with Society of Mind and Documentation Formatter.

    Args:
        society_of_mind: Society of Mind agent wrapping standards team.
        documentation_formatter: Documentation Formatter agent.

    Returns:
        RoundRobinGroupChat: Configured final team.
    """
    return RoundRobinGroupChat(
        participants=[society_of_mind, documentation_formatter],
        max_turns=MAX_OUTER_TURNS,
    )


def print_header(query: str) -> None:
    """
    Print formatted header with query information.

    Args:
        query: User query to display.
    """
    print(f"\n{SEPARATOR}")
    print("ZenTH ISO Standards Coach - Medical Device Compliance Assistant")
    print(SEPARATOR)
    print(f"\nQuery: {query}\n")
    print(SEPARATOR)


def print_welcome_message() -> None:
    """Print welcome message and usage instructions."""
    print("\n" + SEPARATOR)
    print("Welcome to ZenTH ISO Standards Coach")
    print("Medical Device Compliance Assistant")
    print(SEPARATOR)
    print("\nI can help you with:")
    print("  • ISO 13485:2016 - Quality Management Systems")
    print("  • IEC 62304:2006+A1:2015 - Software Lifecycle")
    print("  • IEC 82304-1:2016 - Health Software Standards")
    print("  • ISO 14971:2019 - Risk Management")
    print(f"\nType '{EXIT_COMMANDS[0]}' or '{EXIT_COMMANDS[1]}' to exit.")
    print(SEPARATOR + "\n")


def get_user_input() -> Optional[str]:
    """
    Get user input from command line.

    Returns:
        Optional[str]: User query or None if exit command entered.
    """
    try:
        user_query = input("\n📋 Your question: ").strip()

        if not user_query:
            print("⚠️  Please enter a question.")
            return None

        if user_query.lower() in EXIT_COMMANDS:
            print("\n👋 Thank you for using ZenTH ISO Standards Coach!")
            print("Stay compliant and safe!\n")
            return None

        return user_query

    except (EOFError, KeyboardInterrupt):
        print("\n\n👋 Session interrupted. Goodbye!\n")
        return None


async def run_consultation(
    final_team: RoundRobinGroupChat,
    query: str
) -> None:
    """
    Run the medical device compliance consultation.

    Args:
        final_team: Configured final team for consultation.
        query: User query about medical device standards.

    Raises:
        RuntimeError: If agent execution fails.
    """
    try:
        print_header(query)
        stream = final_team.run_stream(task=query)
        await Console(stream)
        print(f"\n{SEPARATOR}\n")

    except Exception as e:
        print(f"\n❌ Error during consultation: {e}")
        print("Please try rephrasing your question or check your connection.")
        raise


async def interactive_session() -> None:
    """
    Run an interactive session allowing repeated questions.

    Creates the agent team once and reuses it for multiple queries
    for better performance.
    """
    print_welcome_message()

    try:
        # Initialize model client and agents once
        model_client = create_model_client()

        zenth_coach = create_zenth_coach_agent(model_client)
        compliance_reviewer = create_compliance_reviewer_agent(model_client)
        documentation_formatter = create_documentation_formatter_agent(
            model_client
        )

        standards_team = create_standards_team(
            zenth_coach,
            compliance_reviewer
        )

        society_of_mind = SocietyOfMindAgent(
            name="Medical_Standards_SoM",
            team=standards_team,
            model_client=model_client,
        )

        final_team = create_final_team(
            society_of_mind,
            documentation_formatter
        )

        # Interactive loop
        while True:
            query = get_user_input()

            if query is None:
                break

            try:
                await run_consultation(final_team, query)
            except Exception as e:
                print(f"\n⚠️  Consultation error: {e}")
                print("You can continue with a new question.\n")
                continue

    except EnvironmentError as e:
        print(f"\n❌ Configuration Error: {e}\n")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}\n")


async def run_single_query(query: str) -> None:
    """
    Run a single query consultation (non-interactive mode).

    Args:
        query: User query about medical device standards.
    """
    try:
        model_client = create_model_client()

        zenth_coach = create_zenth_coach_agent(model_client)
        compliance_reviewer = create_compliance_reviewer_agent(model_client)
        documentation_formatter = create_documentation_formatter_agent(
            model_client
        )

        standards_team = create_standards_team(
            zenth_coach,
            compliance_reviewer
        )

        society_of_mind = SocietyOfMindAgent(
            name="Medical_Standards_SoM",
            team=standards_team,
            model_client=model_client,
        )

        final_team = create_final_team(
            society_of_mind,
            documentation_formatter
        )

        await run_consultation(final_team, query)

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        raise


async def main() -> None:
    """
    Main entry point - runs interactive session by default.

    Set SINGLE_QUERY environment variable with a query to run in
    non-interactive mode.
    """
    single_query = os.environ.get("SINGLE_QUERY")

    if single_query:
        # Non-interactive mode - run single query
        await run_single_query(single_query)
    else:
        # Interactive mode - allow repeated questions
        await interactive_session()


if __name__ == "__main__":
    asyncio.run(main())