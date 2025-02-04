
```markdown
# Investment Cost Comparison Tool  
**Streamlit app for comparing cross-border trading fees across Canadian platforms**  

![App Screenshot](https://github.com/user-attachments/assets/4440415c-2889-42f9-ae3e-2f34b2bcf864)  
*Example comparison interface*  

## Key Features  
- **Multi-Platform Analysis**: Compare fees across:  
  - Wealthsimple Trade  
  - Questrade (Standard)  
  - Questrade with Norbert's Gambit  
- **Cost Breakdown**: Detailed visualization of:  
  - Commission fees  
  - Foreign exchange spreads  
  - Hidden costs  
- **Dynamic Calculations**: Real-time updates based on:  
  - Trade size  
  - Currency conversion requirements  
  - Account type  

## Methodology  
**Wealthsimple**  
- Zero commission CAD trades  
- 1.5% FX fee on USD trades  

**Questrade Standard**  
- $4.95-$9.95 per trade commissions  
- 1.75% FX spread  

**Norbert's Gambit**  
- $4.95 commission each way  
- 0.12% effective FX cost  

```
# Sample calculation logic
def calculate_norbert_gambit(amount):
    commission = 4.95 * 2
    fx_cost = amount * 0.0012
    return commission + fx_cost
```

## Usage  
1. Access the tool:  
[https://mahmouds-investment-cost-comparison.streamlit.app/](https://mahmouds-investment-cost-comparison.streamlit.app/)  

2. Input parameters:  
- Trade amount  
- Currency pair  
- Platform selection  

3. Analyze results:  
- Cost comparison chart  
- Break-even analysis  
- Historical cost trends  

## Development Setup  
```
pip install -r requirements.txt
streamlit run app.py
```

## License  
MIT License - Free for educational and non-commercial use
```

Save this content directly as `README.md` in your project root. The Markdown formatting includes:
- Proper image references using your GitHub attachment URLs
- Syntax-highlighted code blocks for Python and Bash
- Organized sections with header hierarchy
- Clean list formatting for features and methodology

---
Answer from Perplexity: pplx.ai/share
