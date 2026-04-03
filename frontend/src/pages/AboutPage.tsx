export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50 py-16">
      <div className="max-w-3xl mx-auto px-6">
        <h1 className="text-4xl font-bold text-slate-900 mb-2">About PyPyCode</h1>
        <p className="text-slate-600 mb-8">Empowering Python developers through focused problem-solving</p>

        <div className="space-y-8">
          <section>
            <h2 className="text-2xl font-semibold text-slate-900 mb-4">Our Mission</h2>
            <p className="text-slate-700 leading-relaxed">
              PyPyCode is dedicated to providing a focused, high-quality platform for Python developers to solve algorithmic problems, improve their coding skills, and compete with developers worldwide. We believe in the power of deliberate practice and community-driven learning.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-slate-900 mb-4">About ISHA Systems LLC</h2>
            <p className="text-slate-700 leading-relaxed">
              ISHA Systems LLC is a technology company focused on building innovative solutions for developers. PyPyCode is our flagship product, designed with the philosophy that quality matters more than quantity. We focus exclusively on Python to provide the best possible experience for Python developers.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-slate-900 mb-4">Why Python Only?</h2>
            <p className="text-slate-700 leading-relaxed">
              We chose to focus exclusively on Python because:
            </p>
            <ul className="list-disc list-inside text-slate-700 space-y-2 mt-4">
              <li>Python is one of the most popular programming languages in the world</li>
              <li>It's ideal for learning algorithms and data structures</li>
              <li>Python's simplicity allows developers to focus on problem-solving logic</li>
              <li>The Python community is vibrant and supportive</li>
              <li>Specialization allows us to provide a better, more focused experience</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-slate-900 mb-4">Key Features</h2>
            <ul className="list-disc list-inside text-slate-700 space-y-2">
              <li><strong>Curated Problems:</strong> Carefully selected algorithmic challenges</li>
              <li><strong>Instant Feedback:</strong> Real-time execution in sandboxed environments</li>
              <li><strong>Global Leaderboard:</strong> Compete with developers worldwide</li>
              <li><strong>Clean Interface:</strong> Distraction-free coding environment</li>
              <li><strong>Google Authentication:</strong> Simple, secure sign-in with Google</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-slate-900 mb-4">Contact Us</h2>
            <p className="text-slate-700 leading-relaxed">
              Have questions or feedback? We'd love to hear from you!
              <br />
              <span className="font-semibold">ISHA Systems LLC</span>
              <br />
              Email: hello@pypycode.com
              <br />
              Website: www.pypycode.com
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-slate-900 mb-4">Legal</h2>
            <p className="text-slate-700 leading-relaxed">
              For more information, please review our <a href="/terms" className="text-emerald-600 hover:text-emerald-700 font-semibold">Terms and Conditions</a> and <a href="/privacy" className="text-emerald-600 hover:text-emerald-700 font-semibold">Privacy Policy</a>.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
