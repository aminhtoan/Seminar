import styles from "./page.module.css";
import DigitalTwinChat from "@/components/DigitalTwinChat";

const journey = [
  {
    period: "2021 - Present",
    role: "Co-Founder & CTO",
    company: "Nebula.io",
    detail:
      "Building proprietary LLM products that help recruiters source, understand, and engage talent with speed and precision.",
  },
  {
    period: "2025 - Present",
    role: "AI Advisor",
    company: "Simplified.Travel",
    detail:
      "Guiding personalization strategy for travel experiences using data-driven AI itinerary systems.",
  },
  {
    period: "2020 - 2025",
    role: "CTO",
    company: "Wynden Stark / GQR Global Markets",
    detail:
      "Led data science and engineering innovation initiatives for one of the fastest growing recruitment organizations.",
  },
  {
    period: "2013 - 2020",
    role: "Founder, CEO, then CTO",
    company: "untapt",
    detail:
      "Created an AI hiring platform based on deep learning and NLP; scaled products and team through acquisition.",
  },
  {
    period: "1995 - 2013",
    role: "Software Engineer to Managing Director",
    company: "IBM and JPMorgan",
    detail:
      "Spent 18 years building mission-critical systems globally, eventually leading 300 developers across major regions.",
  },
];

const portfolioSeeds = [
  "Agentic AI systems for enterprise workflows",
  "GenAI product architecture and technical leadership",
  "Conference keynotes, workshops, and executive advisory",
];

export default function Home() {
  return (
    <div className={styles.page}>
      <div className={styles.orbPrimary} />
      <div className={styles.orbSecondary} />

      <header className={styles.header}>
        <p className={styles.brand}>ED DONNER</p>
        <nav className={styles.nav}>
          <a href="#about">About</a>
          <a href="#journey">Journey</a>
          <a href="#portfolio">Portfolio</a>
          <a href="#digital-twin">Digital Twin</a>
          <a href="#contact">Contact</a>
        </nav>
      </header>

      <main className={styles.main}>
        <section className={styles.hero}>
          <p className={styles.badge}>AI Leader | Founder | Speaker</p>
          <h1>
            Building ambitious AI products where enterprise outcomes meet human
            potential.
          </h1>
          <p className={styles.lede}>
            Co-Founder and CTO at Nebula.io. Former JPMorgan Managing Director.
            Repeat startup founder. Mentor and educator with 400,000+ learners
            across GenAI engineering courses.
          </p>

          <div className={styles.ctas}>
            <a
              className={styles.primaryCta}
              href="https://www.linkedin.com/in/eddonner"
              target="_blank"
              rel="noopener noreferrer"
            >
              LinkedIn Profile
            </a>
            <a
              className={styles.secondaryCta}
              href="https://edwarddonner.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              Personal Website
            </a>
          </div>

          <div className={styles.metrics}>
            <article>
              <h2>400K+</h2>
              <p>AI course enrollments</p>
            </article>
            <article>
              <h2>30+</h2>
              <p>Years in engineering</p>
            </article>
            <article>
              <h2>300</h2>
              <p>Developers led globally</p>
            </article>
          </div>
        </section>

        <section id="about" className={styles.sectionPanel}>
          <p className={styles.sectionLabel}>About Me</p>
          <h2>Technology strategist with a builder&apos;s mindset.</h2>
          <p>
            I started coding at age 8 and still spend weekends experimenting
            with large language models. My work combines rigorous engineering,
            product intuition, and a long-term mission: helping people discover
            the roles where they can thrive.
          </p>
          <p>
            I have built and scaled AI products from startup to acquisition,
            advised leadership teams, and delivered workshops at global events
            including O&apos;Reilly and ODSC.
          </p>
        </section>

        <section id="journey" className={styles.sectionPanel}>
          <p className={styles.sectionLabel}>Career Journey</p>
          <h2>From software engineer to global AI executive.</h2>
          <div className={styles.timeline}>
            {journey.map((item) => (
              <article key={`${item.period}-${item.company}`}>
                <p>{item.period}</p>
                <h3>
                  {item.role} <span>@ {item.company}</span>
                </h3>
                <p>{item.detail}</p>
              </article>
            ))}
          </div>
        </section>

        <section id="portfolio" className={styles.sectionPanel}>
          <p className={styles.sectionLabel}>Portfolio</p>
          <h2>Selected work is launching soon.</h2>
          <p>
            A curated portfolio will be published here in future updates.
            Current focus areas:
          </p>
          <div className={styles.portfolioGrid}>
            {portfolioSeeds.map((item) => (
              <article key={item}>
                <p>{item}</p>
                <a href="#contact">Request details</a>
              </article>
            ))}
          </div>
        </section>

        <section id="digital-twin" className={styles.sectionPanel}>
          <p className={styles.sectionLabel}>AI Digital Twin</p>
          <h2>Ask Ed&apos;s AI twin about his career.</h2>
          <p>
            This assistant is powered by OpenRouter using model
            openai/gpt-oss-120b, with context grounded in Ed&apos;s career
            history and leadership profile.
          </p>
          <DigitalTwinChat />
        </section>

        <section id="contact" className={styles.contactPanel}>
          <h2>Let&apos;s build what matters.</h2>
          <p>
            Open to strategic conversations around enterprise AI, product
            transformation, technical advisory, and speaking opportunities.
          </p>
          <a
            className={styles.primaryCta}
            href="https://www.linkedin.com/in/eddonner"
            target="_blank"
            rel="noopener noreferrer"
          >
            Connect on LinkedIn
          </a>
        </section>
      </main>

      <footer className={styles.footer}>
        <p>Ed Donner</p>
        <p>Co-Founder & CTO, Nebula.io</p>
      </footer>
    </div>
  );
}
