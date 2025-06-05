import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LlamaProcessor:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("LLAMA_API_KEY"), 
            base_url="https://api.llama.com/compat/v1/"
        )
    
    def load_person_data(self, filename="person_data.json"):
        """
        Load person data from JSON file
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"❌ Error: {filename} not found. Please run crustdata.py first.")
            return None
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON in {filename}")
            return None
    
    def analyze_job_fit(self, job_description, filename="person_data.json"):
        """
        Analyze if the person is a good fit for a specific job
        """
        person_data = self.load_person_data(filename)
        if not person_data:
            return "Unable to load person data."
        
        # Handle list format from CrustData API
        if isinstance(person_data, list) and len(person_data) > 0:
            person = person_data[0]  # Get the first person
        else:
            person = person_data
        
        prompt = self._create_job_fit_prompt(person, job_description)
        
        try:
            completion = self.client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error processing with Llama API: {str(e)}"
    
    def general_analysis(self, filename="person_data.json"):
        """
        General professional analysis of the person
        """
        person_data = self.load_person_data(filename)
        if not person_data:
            return "Unable to load person data."
        
        # Handle list format from CrustData API
        if isinstance(person_data, list) and len(person_data) > 0:
            person = person_data[0]  # Get the first person
        else:
            person = person_data
        
        prompt = self._create_general_prompt(person)
        
        try:
            completion = self.client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error processing with Llama API: {str(e)}"
    
    def generate_outreach_email(self, job_description, company_name="", role_title="", filename="person_data.json"):
        """
        Generate a personalized outreach email for a candidate
        """
        person_data = self.load_person_data(filename)
        if not person_data:
            return "Unable to load person data."
        
        # Handle list format from CrustData API
        if isinstance(person_data, list) and len(person_data) > 0:
            person = person_data[0]  # Get the first person
        else:
            person = person_data
        
        prompt = f"""
        OUTREACH EMAIL GENERATION REQUEST
        
        COMPLETE CANDIDATE DATA:
        {json.dumps(person, indent=2)}
        
        JOB/OPPORTUNITY DETAILS:
        Role Title: {role_title}
        Company: {company_name}
        Job Description: {job_description}
        
        TASK:
        Write a personalized, professional outreach email to this candidate. The email should:
        
        1. **Subject Line**: Create an engaging subject line
        2. **Personalized Opening**: Reference specific details from their background
        3. **Value Proposition**: Explain why this opportunity would be interesting to them
        4. **Specific Fit**: Mention 2-3 specific aspects of their experience that make them a great fit
        5. **Soft Approach**: Don't be too aggressive or salesy
        6. **Clear CTA**: Include a clear but low-pressure call to action
        7. **Professional Tone**: Warm but professional
        
        Use ALL available information from their profile to make it as personalized as possible.
        Include details like their current role, company, education, previous experience, etc.
        
        Format the response as:
        **Subject:** [subject line]
        
        **Email Body:**
        [email content]
        """
        
        try:
            completion = self.client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error generating email: {str(e)}"

    def simple_chat(self, filename="person_data.json"):
        """
        Simple chat interface to ask questions about the person data
        """
        person_data = self.load_person_data(filename)
        if not person_data:
            return "Unable to load person data."
        
        # Handle list format from CrustData API
        if isinstance(person_data, list) and len(person_data) > 0:
            person = person_data[0]  # Get the first person
        else:
            person = person_data
        
        print("\n🤖 Simple Chat Mode - Ask me anything about the person data!")
        print("Type 'quit' to exit.\n")
        
        while True:
            user_question = input("You: ").strip()
            
            if user_question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_question:
                continue
            
            # Create a simple prompt with the person data and user question
            prompt = f"""
            Based on the following person data, please answer the user's question:

            Person Data:
            {json.dumps(person, indent=2)}

            User Question: {user_question}

            Please provide a helpful and accurate answer based on the data above.
            """
            
            try:
                completion = self.client.chat.completions.create(
                    model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                )
                response = completion.choices[0].message.content
                print(f"\n🤖 Assistant: {response}\n")
            except Exception as e:
                print(f"❌ Error: {str(e)}\n")

    def _create_job_fit_prompt(self, person_data, job_description):
        """
        Create a prompt to analyze job fit using ALL available data
        """
        prompt = f"""
        JOB FIT ANALYSIS REQUEST
        
        COMPLETE CANDIDATE DATA (All Available Information):
        {json.dumps(person_data, indent=2)}
        
        JOB DESCRIPTION:
        {job_description}
        
        ANALYSIS REQUEST:
        Please analyze if this candidate is a good fit for the job described above using ALL the data provided. Provide:
        
        1. **FIT SCORE** (1-10): Rate how well this candidate matches the job requirements
        
        2. **STRENGTHS**: What makes this candidate a good fit? List specific experiences, skills, or qualifications that align with the job. Reference specific details from their complete profile.
        
        3. **GAPS**: What are the potential gaps or concerns? What might the candidate lack for this role?
        
        4. **RECOMMENDATION**: Should we proceed with this candidate? Why or why not?
        
        5. **NEXT STEPS**: If moving forward, what questions should we ask in an interview to validate fit?
        
        6. **OUTREACH EMAIL**: If this is a good fit (score 7+ out of 10), write a personalized professional email that we could send to reach out to this candidate. The email should:
           - Be warm and professional
           - Reference specific aspects of their background that make them a great fit
           - Mention the opportunity without being too salesy
           - Include a clear call to action
           - Be personalized using details from their profile
           - Keep it concise but compelling
        
        Format your response clearly with the numbered sections above.
        """
        
        return prompt
    
    def _create_general_prompt(self, person_data):
        """
        Create a general analysis prompt using ALL available data
        """
        prompt = f"""
        PROFESSIONAL PROFILE ANALYSIS
        
        COMPLETE CANDIDATE DATA (All Available Information):
        {json.dumps(person_data, indent=2)}
        
        Please provide a comprehensive professional analysis using ALL the data provided above including:
        
        1. **Professional Summary**: Brief overview of their career using all available details
        2. **Key Strengths**: Core skills and expertise areas found in the data
        3. **Career Progression**: How their career has evolved based on complete work history
        4. **Industry Focus**: What industries/domains they specialize in
        5. **Unique Value**: What makes them stand out based on their full profile
        6. **Network & Connections**: Any notable connections, companies, or experiences
        7. **Potential Opportunities**: Types of roles they'd be excellent for
        8. **Contact Strategy**: Best approach to reach out to this person based on their profile
        
        Use ALL available information in the JSON data to provide the most comprehensive analysis possible.
        Format your response in a clear, structured way.
        """
        
        return prompt

def main():
    """
    Main function to run job fit analysis
    """
    processor = LlamaProcessor()
    
    print("=== LLAMA AI PROCESSOR ===\n")
    
    # Check if person data exists
    if not os.path.exists("person_data.json"):
        print("❌ No person data found. Please run 'python crustdata.py' first to fetch data.")
        return
    
    print("Choose analysis type:")
    print("1. Job Fit Analysis (compare candidate to job description)")
    print("2. General Professional Analysis")
    print("3. Simple Chat (ask questions about the person data)")
    print("4. Generate Outreach Email")
    
    choice = input("\nEnter your choice (1, 2, 3, or 4): ").strip()
    
    if choice == "1":
        print("\n📝 Please enter the job description:")
        job_description = input()
        
        if job_description.strip():
            print("\n🤖 Analyzing job fit...")
            result = processor.analyze_job_fit(job_description)
            print("\n" + "="*50)
            print("JOB FIT ANALYSIS RESULTS")
            print("="*50)
            print(result)
        else:
            print("❌ Job description cannot be empty.")
    
    elif choice == "2":
        print("\n🤖 Performing general analysis...")
        result = processor.general_analysis()
        print("\n" + "="*50)
        print("PROFESSIONAL ANALYSIS RESULTS")
        print("="*50)
        print(result)
    
    elif choice == "3":
        processor.simple_chat()
    
    elif choice == "4":
        print("\n📧 Generating outreach email...")
        print("\nEnter the job description:")
        job_description = input()
        print("\nEnter the company name (optional):")
        company_name = input()
        print("\nEnter the role title (optional):")
        role_title = input()
        
        if job_description.strip():
            print("\n🤖 Generating personalized email...")
            result = processor.generate_outreach_email(job_description, company_name, role_title)
            print("\n" + "="*50)
            print("OUTREACH EMAIL")
            print("="*50)
            print(result)
        else:
            print("❌ Job description cannot be empty.")
    
    else:
        print("❌ Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
