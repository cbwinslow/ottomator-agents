"""
Innovative Agent Combinations - Creates new and unique agent combinations
for maximum value and proof-of-concept demonstrations
"""

from typing import Dict, List, Any
from agent_registry import AgentRegistry, AgentCombination
from combination_engine import CombinationEngine
from config_manager import ConfigurationManager

class InnovativeAgentCombinations:
    """Creates innovative and unconventional agent combinations"""
    
    def __init__(self, registry: AgentRegistry, config_manager: ConfigurationManager):
        self.registry = registry
        self.config_manager = config_manager
    
    def create_all_innovative_combinations(self) -> List[str]:
        """Create all innovative agent combinations"""
        combinations_created = []
        
        # Cross-domain combinations
        combinations_created.extend(self._create_cross_domain_combinations())
        
        # Multi-modal intelligence combinations
        combinations_created.extend(self._create_multimodal_combinations())
        
        # Specialized workflow combinations
        combinations_created.extend(self._create_specialized_workflows())
        
        # Experimental and proof-of-concept combinations
        combinations_created.extend(self._create_experimental_combinations())
        
        # Chain-reaction combinations
        combinations_created.extend(self._create_chain_reaction_combinations())
        
        return combinations_created
    
    def _create_cross_domain_combinations(self) -> List[str]:
        """Create combinations that bridge different domains"""
        combinations = []
        
        # AI-Powered Investment Research Suite
        ai_investment_combo = AgentCombination(
            name="ai-investment-research-suite",
            description="Comprehensive investment research combining market analysis, news sentiment, and financial modeling",
            component_agents=[
                "advanced-web-researcher",      # Market research
                "ask-reddit-agent",             # Retail investor sentiment
                "youtube-summary-agent",        # Financial news analysis
                "genericsuite-app-maker-agent", # Financial model generation
                "intelligent-invoicing-agent"   # Cost analysis
            ],
            workflow={
                "type": "conditional",
                "steps": [
                    {
                        "step_id": "market_research",
                        "agent_name": "advanced-web-researcher",
                        "action": "research",
                        "description": "Research market trends and company fundamentals",
                        "inputs": {"query": "${investment_target} market analysis trends financials"},
                        "timeout": 400
                    },
                    {
                        "step_id": "sentiment_analysis", 
                        "agent_name": "ask-reddit-agent",
                        "action": "analyze",
                        "description": "Analyze retail investor sentiment",
                        "inputs": {"query": "${investment_target} stock discussion opinion"},
                        "timeout": 300
                    },
                    {
                        "step_id": "news_summary",
                        "agent_name": "youtube-summary-agent", 
                        "action": "summarize",
                        "description": "Summarize financial news and analysis videos",
                        "inputs": {"query": "${investment_target} financial news analysis"},
                        "timeout": 350
                    },
                    {
                        "step_id": "financial_model",
                        "agent_name": "genericsuite-app-maker-agent",
                        "action": "generate",
                        "description": "Generate financial analysis models",
                        "inputs": {
                            "research_data": "${market_research}",
                            "sentiment_data": "${sentiment_analysis}",
                            "news_data": "${news_summary}"
                        },
                        "timeout": 500
                    },
                    {
                        "step_id": "cost_analysis",
                        "agent_name": "intelligent-invoicing-agent",
                        "action": "analyze",
                        "description": "Analyze investment costs and fees",
                        "inputs": {"investment_data": "${financial_model}"},
                        "timeout": 200
                    }
                ]
            },
            benefits=[
                "Comprehensive investment analysis from multiple perspectives",
                "Combines technical analysis with sentiment analysis",
                "Generates actionable financial models",
                "Includes cost analysis for informed decisions",
                "Integrates both professional and retail investor insights"
            ],
            use_cases=[
                "Individual stock analysis",
                "Portfolio optimization research", 
                "Market sector analysis",
                "Investment thesis validation",
                "Risk assessment and due diligence"
            ]
        )
        self.registry.combinations[ai_investment_combo.name] = ai_investment_combo
        combinations.append(ai_investment_combo.name)
        
        # Global Real Estate Intelligence Network
        real_estate_intel_combo = AgentCombination(
            name="global-real-estate-intelligence-network",
            description="Multi-region real estate analysis combining local expertise with global trends",
            component_agents=[
                "gilbert-real-estate-agent",    # US real estate
                "bali-property-agent",          # International property
                "travel-agent",                 # Location analysis
                "advanced-web-researcher",      # Market trends
                "linkedin-x-blog-content-creator" # Marketing content
            ],
            workflow={
                "type": "parallel",
                "steps": [
                    {
                        "step_id": "us_market_analysis",
                        "agent_name": "gilbert-real-estate-agent",
                        "action": "analyze",
                        "description": "Analyze US real estate market",
                        "inputs": {"location": "${target_location}", "property_type": "${property_type}"},
                        "timeout": 400
                    },
                    {
                        "step_id": "international_analysis",
                        "agent_name": "bali-property-agent", 
                        "action": "analyze",
                        "description": "Analyze international property markets",
                        "inputs": {"region": "${target_region}", "investment_type": "${investment_type}"},
                        "timeout": 400
                    },
                    {
                        "step_id": "location_intelligence",
                        "agent_name": "travel-agent",
                        "action": "research",
                        "description": "Research location amenities and lifestyle factors",
                        "inputs": {"destination": "${target_location}"},
                        "timeout": 300
                    },
                    {
                        "step_id": "market_trends",
                        "agent_name": "advanced-web-researcher",
                        "action": "research", 
                        "description": "Research global real estate trends",
                        "inputs": {"query": "real estate trends ${target_location} market analysis"},
                        "timeout": 350
                    }
                ]
            },
            benefits=[
                "Global perspective on real estate investments",
                "Multi-region market comparison",
                "Lifestyle and amenity analysis",
                "Investment opportunity identification",
                "Marketing content for real estate professionals"
            ],
            use_cases=[
                "International property investment",
                "Relocation planning",
                "Real estate market research",
                "Investment portfolio diversification",
                "Property development feasibility"
            ]
        )
        self.registry.combinations[real_estate_intel_combo.name] = real_estate_intel_combo
        combinations.append(real_estate_intel_combo.name)
        
        return combinations
    
    def _create_multimodal_combinations(self) -> List[str]:
        """Create combinations that handle multiple content types"""
        combinations = []
        
        # Omnimedia Content Intelligence Platform
        omnimedia_combo = AgentCombination(
            name="omnimedia-content-intelligence-platform",
            description="Comprehensive content analysis across text, video, and social media platforms",
            component_agents=[
                "youtube-video-summarizer",     # Video content
                "ask-reddit-agent",             # Text discussions
                "tweet-generator-agent",        # Social media
                "crawl4AI-agent",              # Web content
                "agentic-rag-knowledge-graph", # Knowledge synthesis
                "streambuzz-agent"             # Media trends
            ],
            workflow={
                "type": "sequential",
                "steps": [
                    {
                        "step_id": "video_analysis",
                        "agent_name": "youtube-video-summarizer",
                        "action": "analyze",
                        "description": "Analyze video content and trends",
                        "inputs": {"topic": "${content_topic}"},
                        "timeout": 400
                    },
                    {
                        "step_id": "discussion_analysis",
                        "agent_name": "ask-reddit-agent",
                        "action": "analyze", 
                        "description": "Analyze discussion forums and communities",
                        "inputs": {"query": "${content_topic}"},
                        "timeout": 350
                    },
                    {
                        "step_id": "web_content_analysis",
                        "agent_name": "crawl4AI-agent",
                        "action": "crawl",
                        "description": "Crawl and analyze web content",
                        "inputs": {"search_query": "${content_topic}"},
                        "timeout": 450
                    },
                    {
                        "step_id": "media_trends",
                        "agent_name": "streambuzz-agent",
                        "action": "analyze",
                        "description": "Analyze streaming and media trends",
                        "inputs": {"topic": "${content_topic}"},
                        "timeout": 300
                    },
                    {
                        "step_id": "knowledge_synthesis",
                        "agent_name": "agentic-rag-knowledge-graph",
                        "action": "synthesize",
                        "description": "Create knowledge graph from all sources",
                        "inputs": {
                            "video_data": "${video_analysis}",
                            "discussion_data": "${discussion_analysis}",
                            "web_data": "${web_content_analysis}",
                            "media_data": "${media_trends}"
                        },
                        "timeout": 500
                    },
                    {
                        "step_id": "content_generation",
                        "agent_name": "tweet-generator-agent",
                        "action": "generate",
                        "description": "Generate cross-platform content",
                        "inputs": {"synthesis": "${knowledge_synthesis}"},
                        "timeout": 250
                    }
                ]
            },
            benefits=[
                "360-degree content analysis across all major platforms",
                "Cross-media trend identification", 
                "Comprehensive knowledge graph creation",
                "Multi-format content generation",
                "Real-time media intelligence"
            ],
            use_cases=[
                "Brand monitoring and analysis",
                "Content strategy development",
                "Trend forecasting",
                "Competitive intelligence",
                "Crisis communication planning"
            ]
        )
        self.registry.combinations[omnimedia_combo.name] = omnimedia_combo
        combinations.append(omnimedia_combo.name)
        
        return combinations
    
    def _create_specialized_workflows(self) -> List[str]:
        """Create highly specialized workflow combinations"""
        combinations = []
        
        # AI-Powered Academic Research Pipeline
        academic_research_combo = AgentCombination(
            name="ai-powered-academic-research-pipeline",
            description="End-to-end academic research from literature review to publication",
            component_agents=[
                "advanced-web-researcher",      # Literature search
                "agentic-rag-knowledge-graph", # Knowledge organization
                "foundational-rag-agent",      # Reference management
                "genericsuite-app-maker-agent", # Paper structure
                "linkedin-x-blog-content-creator" # Academic writing
            ],
            workflow={
                "type": "sequential",
                "steps": [
                    {
                        "step_id": "literature_search",
                        "agent_name": "advanced-web-researcher",
                        "action": "research",
                        "description": "Comprehensive literature search",
                        "inputs": {"query": "${research_topic} academic papers research"},
                        "timeout": 500
                    },
                    {
                        "step_id": "knowledge_mapping",
                        "agent_name": "agentic-rag-knowledge-graph",
                        "action": "map",
                        "description": "Create research knowledge graph",
                        "inputs": {"literature": "${literature_search}"},
                        "timeout": 400
                    },
                    {
                        "step_id": "reference_analysis",
                        "agent_name": "foundational-rag-agent",
                        "action": "analyze",
                        "description": "Analyze references and citations",
                        "inputs": {"knowledge_graph": "${knowledge_mapping}"},
                        "timeout": 350
                    },
                    {
                        "step_id": "paper_structure",
                        "agent_name": "genericsuite-app-maker-agent",
                        "action": "structure",
                        "description": "Generate paper outline and structure",
                        "inputs": {"research_data": "${reference_analysis}"},
                        "timeout": 300
                    },
                    {
                        "step_id": "academic_writing",
                        "agent_name": "linkedin-x-blog-content-creator",
                        "action": "write",
                        "description": "Generate academic content",
                        "inputs": {"structure": "${paper_structure}", "research": "${reference_analysis}"},
                        "timeout": 600
                    }
                ]
            },
            benefits=[
                "Automated literature review process",
                "Knowledge graph visualization of research domain",
                "Citation analysis and gap identification",
                "Structured academic writing assistance",
                "Research methodology recommendations"
            ],
            use_cases=[
                "PhD dissertation research",
                "Systematic literature reviews",
                "Grant proposal preparation",
                "Conference paper writing",
                "Research collaboration"
            ]
        )
        self.registry.combinations[academic_research_combo.name] = academic_research_combo
        combinations.append(academic_research_combo.name)
        
        # E-commerce Intelligence Ecosystem
        ecommerce_intel_combo = AgentCombination(
            name="ecommerce-intelligence-ecosystem",
            description="Complete e-commerce intelligence from product research to marketing automation",
            component_agents=[
                "crawl4AI-agent-v2",           # Product data scraping
                "ask-reddit-agent",            # Customer sentiment
                "intelligent-invoicing-agent", # Pricing analysis
                "linkedin-x-blog-content-creator", # Marketing content
                "travel-agent"                 # Logistics analysis
            ],
            workflow={
                "type": "conditional",
                "steps": [
                    {
                        "step_id": "product_research",
                        "agent_name": "crawl4AI-agent-v2",
                        "action": "crawl",
                        "description": "Research product market and competitors",
                        "inputs": {"product_category": "${target_product}"},
                        "timeout": 450
                    },
                    {
                        "step_id": "customer_sentiment",
                        "agent_name": "ask-reddit-agent",
                        "action": "analyze",
                        "description": "Analyze customer reviews and sentiment",
                        "inputs": {"query": "${target_product} reviews experience"},
                        "timeout": 350
                    },
                    {
                        "step_id": "pricing_analysis",
                        "agent_name": "intelligent-invoicing-agent",
                        "action": "analyze",
                        "description": "Analyze pricing strategies and costs",
                        "inputs": {"product_data": "${product_research}"},
                        "timeout": 300
                    },
                    {
                        "step_id": "logistics_optimization",
                        "agent_name": "travel-agent",
                        "action": "optimize",
                        "description": "Optimize shipping and logistics",
                        "inputs": {"product_info": "${product_research}"},
                        "timeout": 250,
                        "conditions": {"has_data": True}
                    },
                    {
                        "step_id": "marketing_content",
                        "agent_name": "linkedin-x-blog-content-creator",
                        "action": "create",
                        "description": "Generate marketing content and campaigns",
                        "inputs": {
                            "product_data": "${product_research}",
                            "sentiment": "${customer_sentiment}",
                            "pricing": "${pricing_analysis}"
                        },
                        "timeout": 400
                    }
                ]
            },
            benefits=[
                "Complete market intelligence for e-commerce",
                "Customer sentiment analysis integration",
                "Pricing optimization recommendations",
                "Logistics and shipping optimization",
                "Automated marketing content generation"
            ],
            use_cases=[
                "Product launch planning",
                "Competitive analysis",
                "Market entry strategy",
                "Supply chain optimization",
                "Customer acquisition campaigns"
            ]
        )
        self.registry.combinations[ecommerce_intel_combo.name] = ecommerce_intel_combo
        combinations.append(ecommerce_intel_combo.name)
        
        return combinations
    
    def _create_experimental_combinations(self) -> List[str]:
        """Create experimental and proof-of-concept combinations"""
        combinations = []
        
        # Quantum Content Generation Network
        quantum_content_combo = AgentCombination(
            name="quantum-content-generation-network",
            description="Experimental multi-agent content generation using quantum-inspired parallel processing",
            component_agents=[
                "genericsuite-app-maker-agent", # Idea generation
                "tweet-generator-agent",        # Micro-content
                "youtube-educator-plus-agent",  # Educational content
                "linkedin-x-blog-content-creator", # Professional content
                "mem0-agent"                    # Memory and learning
            ],
            workflow={
                "type": "parallel",
                "steps": [
                    {
                        "step_id": "idea_quantum_state",
                        "agent_name": "genericsuite-app-maker-agent",
                        "action": "ideate",
                        "description": "Generate multiple idea quantum states",
                        "inputs": {"theme": "${content_theme}", "variants": 5},
                        "timeout": 300
                    },
                    {
                        "step_id": "micro_content_state",
                        "agent_name": "tweet-generator-agent",
                        "action": "generate",
                        "description": "Create micro-content variations",
                        "inputs": {"theme": "${content_theme}", "formats": ["tweet", "linkedin_post", "headline"]},
                        "timeout": 250
                    },
                    {
                        "step_id": "educational_state",
                        "agent_name": "youtube-educator-plus-agent",
                        "action": "educate",
                        "description": "Generate educational content variations",
                        "inputs": {"topic": "${content_theme}", "learning_styles": ["visual", "auditory", "kinesthetic"]},
                        "timeout": 400
                    },
                    {
                        "step_id": "professional_state",
                        "agent_name": "linkedin-x-blog-content-creator",
                        "action": "create",
                        "description": "Create professional content variations",
                        "inputs": {"subject": "${content_theme}", "audiences": ["executives", "professionals", "entrepreneurs"]},
                        "timeout": 350
                    },
                    {
                        "step_id": "memory_consolidation",
                        "agent_name": "mem0-agent",
                        "action": "consolidate",
                        "description": "Learn from all content variations",
                        "inputs": {
                            "ideas": "${idea_quantum_state}",
                            "micro": "${micro_content_state}",
                            "educational": "${educational_state}",
                            "professional": "${professional_state}"
                        },
                        "timeout": 200
                    }
                ]
            },
            benefits=[
                "Simultaneous multi-format content generation",
                "Quantum-inspired parallel processing approach",
                "Cross-pollination of ideas between formats",
                "Memory-enhanced learning from all variations",
                "Exponential content variation possibilities"
            ],
            use_cases=[
                "Content experiment laboratories",
                "A/B testing content generation",
                "Multi-platform campaign development",
                "Creative brainstorming sessions",
                "Content format optimization"
            ]
        )
        self.registry.combinations[quantum_content_combo.name] = quantum_content_combo
        combinations.append(quantum_content_combo.name)
        
        # Hybrid Human-AI Research Collective
        hybrid_research_combo = AgentCombination(
            name="hybrid-human-ai-research-collective",
            description="Experimental combination simulating human research team dynamics with AI agents",
            component_agents=[
                "general-researcher-agent",     # Lead researcher
                "advanced-web-researcher",      # Research specialist
                "agentic-rag-knowledge-graph", # Knowledge manager
                "nba-agent",                   # Data analyst (unconventional use)
                "tech-stack-expert"            # Technical advisor
            ],
            workflow={
                "type": "conditional",
                "steps": [
                    {
                        "step_id": "research_planning",
                        "agent_name": "general-researcher-agent",
                        "action": "plan",
                        "description": "Create research methodology and plan",
                        "inputs": {"research_question": "${research_question}"},
                        "timeout": 300
                    },
                    {
                        "step_id": "data_collection",
                        "agent_name": "advanced-web-researcher",
                        "action": "collect",
                        "description": "Collect research data systematically",
                        "inputs": {"methodology": "${research_planning}"},
                        "timeout": 500
                    },
                    {
                        "step_id": "statistical_analysis",
                        "agent_name": "nba-agent",
                        "action": "analyze",
                        "description": "Perform statistical analysis (repurposed for general data)",
                        "inputs": {"data": "${data_collection}"},
                        "timeout": 350
                    },
                    {
                        "step_id": "knowledge_synthesis",
                        "agent_name": "agentic-rag-knowledge-graph",
                        "action": "synthesize",
                        "description": "Create knowledge synthesis and insights",
                        "inputs": {"analysis": "${statistical_analysis}", "raw_data": "${data_collection}"},
                        "timeout": 400
                    },
                    {
                        "step_id": "technical_validation",
                        "agent_name": "tech-stack-expert",
                        "action": "validate",
                        "description": "Validate methodology and technical aspects",
                        "inputs": {"synthesis": "${knowledge_synthesis}"},
                        "timeout": 250,
                        "conditions": {"previous_step_success": True}
                    }
                ]
            },
            benefits=[
                "Simulates human research team collaboration",
                "Combines different analytical perspectives",
                "Multi-disciplinary approach to research",
                "Unconventional agent repurposing for creativity",
                "Hierarchical research validation process"
            ],
            use_cases=[
                "Interdisciplinary research projects",
                "Research methodology validation",
                "Academic collaboration simulation",
                "Cross-domain knowledge transfer",
                "Research process optimization"
            ]
        )
        self.registry.combinations[hybrid_research_combo.name] = hybrid_research_combo
        combinations.append(hybrid_research_combo.name)
        
        return combinations
    
    def _create_chain_reaction_combinations(self) -> List[str]:
        """Create combinations that trigger chain reactions of insights"""
        combinations = []
        
        # Viral Content Evolution Engine
        viral_evolution_combo = AgentCombination(
            name="viral-content-evolution-engine",
            description="Creates content that evolves and adapts based on social feedback loops",
            component_agents=[
                "tweet-generator-agent",        # Initial content seed
                "ask-reddit-agent",            # Community feedback
                "youtube-summary-agent",       # Viral video analysis
                "streambuzz-agent",            # Trend tracking
                "linkedin-x-blog-content-creator" # Content evolution
            ],
            workflow={
                "type": "sequential",
                "steps": [
                    {
                        "step_id": "content_seed",
                        "agent_name": "tweet-generator-agent",
                        "action": "generate",
                        "description": "Generate initial content seeds",
                        "inputs": {"topic": "${viral_topic}", "seed_count": 10},
                        "timeout": 200
                    },
                    {
                        "step_id": "community_feedback",
                        "agent_name": "ask-reddit-agent",
                        "action": "analyze",
                        "description": "Analyze community response patterns",
                        "inputs": {"content_seeds": "${content_seed}"},
                        "timeout": 350
                    },
                    {
                        "step_id": "viral_pattern_analysis",
                        "agent_name": "youtube-summary-agent",
                        "action": "analyze",
                        "description": "Analyze viral content patterns",
                        "inputs": {"topic": "${viral_topic}"},
                        "timeout": 300
                    },
                    {
                        "step_id": "trend_momentum",
                        "agent_name": "streambuzz-agent",
                        "action": "track",
                        "description": "Track trend momentum and timing",
                        "inputs": {"patterns": "${viral_pattern_analysis}"},
                        "timeout": 250
                    },
                    {
                        "step_id": "content_evolution",
                        "agent_name": "linkedin-x-blog-content-creator",
                        "action": "evolve",
                        "description": "Evolve content based on all feedback",
                        "inputs": {
                            "seeds": "${content_seed}",
                            "feedback": "${community_feedback}",
                            "patterns": "${viral_pattern_analysis}",
                            "momentum": "${trend_momentum}"
                        },
                        "timeout": 400
                    }
                ]
            },
            benefits=[
                "Content that adapts to audience response",
                "Viral pattern recognition and application",
                "Community-driven content evolution",
                "Timing optimization for maximum impact",
                "Cross-platform viral strategy"
            ],
            use_cases=[
                "Viral marketing campaigns",
                "Social media strategy optimization",
                "Influencer content development",
                "Brand awareness campaigns",
                "Community engagement experiments"
            ]
        )
        self.registry.combinations[viral_evolution_combo.name] = viral_evolution_combo
        combinations.append(viral_evolution_combo.name)
        
        # Ecosystem Impact Analyzer
        ecosystem_impact_combo = AgentCombination(
            name="ecosystem-impact-analyzer",
            description="Analyzes ripple effects and ecosystem impacts of decisions across multiple domains",
            component_agents=[
                "small-business-researcher",    # Economic impact
                "travel-agent",                # Environmental/location impact
                "indoor-farming-agent",        # Sustainability impact  
                "tech-stack-expert",           # Technology impact
                "genericsuite-app-maker-agent" # Systems modeling
            ],
            workflow={
                "type": "parallel",
                "steps": [
                    {
                        "step_id": "economic_ripples",
                        "agent_name": "small-business-researcher",
                        "action": "analyze",
                        "description": "Analyze economic ripple effects",
                        "inputs": {"decision": "${impact_scenario}"},
                        "timeout": 350
                    },
                    {
                        "step_id": "environmental_impact",
                        "agent_name": "travel-agent",
                        "action": "assess",
                        "description": "Assess environmental and location impacts",
                        "inputs": {"scenario": "${impact_scenario}"},
                        "timeout": 300
                    },
                    {
                        "step_id": "sustainability_analysis",
                        "agent_name": "indoor-farming-agent",
                        "action": "evaluate",
                        "description": "Evaluate sustainability implications",
                        "inputs": {"impact_type": "${impact_scenario}"},
                        "timeout": 350
                    },
                    {
                        "step_id": "technology_consequences",
                        "agent_name": "tech-stack-expert",
                        "action": "analyze",
                        "description": "Analyze technology adoption consequences",
                        "inputs": {"decision": "${impact_scenario}"},
                        "timeout": 300
                    },
                    {
                        "step_id": "systems_modeling",
                        "agent_name": "genericsuite-app-maker-agent",
                        "action": "model",
                        "description": "Create systems model of all impacts",
                        "inputs": {
                            "economic": "${economic_ripples}",
                            "environmental": "${environmental_impact}",
                            "sustainability": "${sustainability_analysis}",
                            "technology": "${technology_consequences}"
                        },
                        "timeout": 450
                    }
                ]
            },
            benefits=[
                "Holistic impact assessment across domains",
                "Unintended consequence identification",
                "Systems thinking approach to decision making",
                "Multi-dimensional risk analysis",
                "Sustainability impact quantification"
            ],
            use_cases=[
                "Policy impact assessment",
                "Corporate decision analysis",
                "Environmental impact studies",
                "Technology adoption planning",
                "Urban planning and development"
            ]
        )
        self.registry.combinations[ecosystem_impact_combo.name] = ecosystem_impact_combo
        combinations.append(ecosystem_impact_combo.name)
        
        return combinations
    
    def get_combination_matrix(self) -> Dict[str, List[str]]:
        """Generate a matrix of potential agent combinations"""
        agents_by_category = {}
        for agent in self.registry.agents.values():
            if agent.category not in agents_by_category:
                agents_by_category[agent.category] = []
            agents_by_category[agent.category].append(agent.name)
        
        # Generate potential combinations
        combination_matrix = {}
        
        for primary_category, primary_agents in agents_by_category.items():
            combination_matrix[primary_category] = []
            
            # Find complementary categories
            for secondary_category, secondary_agents in agents_by_category.items():
                if secondary_category != primary_category:
                    # Create potential combinations
                    for primary_agent in primary_agents[:2]:  # Limit to avoid explosion
                        for secondary_agent in secondary_agents[:2]:
                            combo_name = f"{primary_agent}+{secondary_agent}"
                            combination_matrix[primary_category].append(combo_name)
        
        return combination_matrix

if __name__ == "__main__":
    # Test innovative combinations
    from agent_registry import AgentRegistry
    from config_manager import ConfigurationManager
    
    registry = AgentRegistry()
    registry.discover_agents()
    
    config_manager = ConfigurationManager()
    
    innovative = InnovativeAgentCombinations(registry, config_manager)
    
    print("Creating innovative agent combinations...")
    created = innovative.create_all_innovative_combinations()
    
    print(f"Created {len(created)} innovative combinations:")
    for combo_name in created:
        combo = registry.combinations[combo_name]
        print(f"\n🚀 {combo.name}")
        print(f"   Description: {combo.description}")
        print(f"   Components: {', '.join(combo.component_agents)}")
        print(f"   Benefits: {len(combo.benefits)} key benefits")
        print(f"   Use cases: {len(combo.use_cases)} use cases")
    
    print(f"\nTotal combinations now available: {len(registry.combinations)}")
    
    # Show combination matrix
    matrix = innovative.get_combination_matrix()
    print(f"\nPotential combination opportunities:")
    for category, combos in matrix.items():
        print(f"{category}: {len(combos)} potential combinations")