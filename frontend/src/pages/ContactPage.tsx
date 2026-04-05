import { useState, useEffect } from "react";
import { api } from "../utils/api";
import { useAuthStore } from "../hooks/useAuth";

interface ContactFormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

export default function ContactPage() {
  const { user } = useAuthStore();
  const [formData, setFormData] = useState<ContactFormData>({
    name: "",
    email: "",
    subject: "",
    message: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  // Populate form with user data when logged in
  useEffect(() => {
    if (user) {
      setFormData(prev => ({
        ...prev,
        name: user.username || "",
        email: user.email || "",
      }));
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus("idle");
    setErrorMessage("");

    try {
      const response = await api.post("/contact/", formData);
      if (response) {
        setSubmitStatus("success");
        setFormData({
          name: user?.username || "",
          email: user?.email || "",
          subject: "",
          message: "",
        });
      }
    } catch (error: any) {
      setSubmitStatus("error");
      setErrorMessage(error?.message || "Failed to submit your message. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const isFormValid = formData.name.trim() && 
                     formData.email.trim() && 
                     formData.subject.trim() && 
                     formData.message.trim() &&
                     formData.email.includes("@") && 
                     formData.email.includes(".");

  return (
    <div className="min-h-[calc(100vh-64px)] bg-gradient-to-b from-slate-50 via-white to-slate-50">
      {/* Background glow */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-emerald-500/5 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 right-0 w-80 h-80 bg-blue-500/3 rounded-full blur-[100px]" />
      </div>

      <div className="relative max-w-2xl mx-auto px-6 py-16">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-slate-900 mb-4">
            Contact Us
          </h1>
          <p className="text-lg text-slate-600 max-w-md mx-auto">
            Have a question, feedback, or need help? We'd love to hear from you.
          </p>
        </div>

        {/* Contact Form */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-xl p-8">
          {submitStatus === "success" ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-slate-900 mb-2">
                Message Sent Successfully!
              </h3>
              <p className="text-slate-600 mb-6">
                Thank you for contacting us. We'll get back to you as soon as possible.
              </p>
              <button
                onClick={() => {
                  setSubmitStatus("idle");
                  setFormData({
                    name: user?.username || "",
                    email: user?.email || "",
                    subject: "",
                    message: "",
                  });
                }}
                className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
              >
                Send Another Message
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Name Field */}
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-2">
                  Name *
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  readOnly={!!user}
                  className={`w-full px-4 py-3 border border-slate-200 rounded-lg transition-all ${
                    user 
                      ? 'bg-gray-100 text-slate-600 cursor-not-allowed' 
                      : 'bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent focus:bg-gray-50'
                  }`}
                  placeholder={user ? "" : "Your full name"}
                />
              </div>

              {/* Email Field */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-2">
                  Email *
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  readOnly={!!user}
                  className={`w-full px-4 py-3 border border-slate-200 rounded-lg transition-all ${
                    user 
                      ? 'bg-gray-100 text-slate-600 cursor-not-allowed' 
                      : 'bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent focus:bg-gray-50'
                  }`}
                  placeholder={user ? "" : "your.email@example.com"}
                />
              </div>

              {/* Subject Field */}
              <div>
                <label htmlFor="subject" className="block text-sm font-medium text-slate-700 mb-2">
                  Subject *
                </label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-slate-200 rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent focus:bg-gray-50 transition-all"
                  placeholder="What is this regarding?"
                />
              </div>

              {/* Message Field */}
              <div>
                <label htmlFor="message" className="block text-sm font-medium text-slate-700 mb-2">
                  Message *
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={6}
                  className="w-full px-4 py-3 border border-slate-200 rounded-lg bg-slate-50 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent focus:bg-white transition-all resize-none"
                  placeholder="Tell us more about your question or feedback..."
                />
              </div>

              {/* Error Message */}
              {submitStatus === "error" && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex items-center">
                    <svg className="w-5 h-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span className="text-red-700">{errorMessage}</span>
                  </div>
                </div>
              )}

              {/* Submit Button */}
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={!isFormValid || isSubmitting}
                  className="px-8 py-3 bg-emerald-600 text-white font-medium rounded-lg hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                  {isSubmitting ? (
                    <div className="flex items-center">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                      Sending...
                    </div>
                  ) : (
                    "Send Message"
                  )}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
